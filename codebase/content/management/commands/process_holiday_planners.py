import calendar
import locale
import random
from copy import copy
from datetime import datetime
from pathlib import Path

import xlwings as xw
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from py_markdown_table.markdown_table import markdown_table

from tex.compile import render_pdf
from tex.values import LATEX_LANGUAGES

from ...listing_types.calendar import create_calendar
from ...texts import TEXT_COUNTRIES, TEXT_DATE, TEXT_HOLIDAY, TEXT_WEEKDAY

TOPIC_SLUG = "public-holidays"
COLUMN_START = 4


class Holiday(object):
    def __init__(self, date, title) -> None:
        self.date = date
        self.title = title

    def tex_date(self):
        return self.date.strftime("%Y-%m-%d")


def get_excel_file(dirname, filename):
    return settings.BASE_DIR / "material" / "listings" / dirname / "files" / filename


class Command(BaseCommand):
    help = "Create body.md articles from the Excel files (holiday-planners)"

    @transaction.atomic
    def handle(self, *args, **options):
        # From: material/holiday-planners/<Excel-files>
        # To: articles_md/<lang>/<TOPIC_SLUG>/<article_title>/body.md
        self.stdout.write("Processing...")
        extract_information_from_excel(
            excel_file=get_excel_file(
                "2024_Urlaubsplaner_de", "2024_Urlaubsplaner.xlsx"
            ),
            year=2024,
            langs=["de"],
            sheet_codes=["DE", "AT", "CH"],
        )
        extract_information_from_excel(
            excel_file=get_excel_file(
                "2025_Urlaubsplaner_de", "2025_Urlaubsplaner.xlsx"
            ),
            year=2025,
            langs=["de"],
            sheet_codes=["DE", "AT", "CH"],
        )
        extract_information_from_excel(
            excel_file=get_excel_file(
                "2024_PlanificacionDeVacaciones_es",
                "2024_PlanificacionDeVacaciones.xlsx",
            ),
            year=2024,
            langs=["es"],
            sheet_codes=["ES"],
        )

        self.stdout.write("Done.")


def extract_information_from_excel(
    excel_file=None, year=None, langs=[], sheet_codes=[]
):
    for country_code in sheet_codes:
        sheet = xw.Book(excel_file).sheets[country_code]
        col_end = len(sheet.used_range.value[0])
        row_end = len(sheet.used_range.value)
        holiday_v = sheet.range((2, 1), (row_end, 1)).value
        for lang in langs:
            locale.setlocale(locale.LC_TIME, lang)
            for col in range(COLUMN_START, col_end):
                table_data = []
                holidays_part1 = []
                holidays_part2 = []
                state = sheet.cells(1, col).value
                date_v = sheet.range((2, col), (row_end, col)).value

                for index, date in enumerate(date_v):
                    if date is None:
                        continue
                    emoji = get_weekday_emoji(date.weekday())
                    weekday_text = str(calendar.day_name[date.weekday()]).capitalize()
                    table_data.append(
                        {
                            f"**{TEXT_HOLIDAY[lang]}**": holiday_v[index],
                            f"**{TEXT_DATE[lang]}**": date.strftime("%x"),
                            f"**{TEXT_WEEKDAY[lang]}**": f"{emoji} {weekday_text}",
                        }
                    )
                    if date < datetime(year, 6, 1):
                        holidays_part1.append(Holiday(date, holiday_v[index]))
                    else:
                        holidays_part2.append(Holiday(date, holiday_v[index]))

                md_table = (
                    markdown_table(table_data)
                    .set_params(row_sep="markdown", quote=False)
                    .get_markdown()
                )

                context = {
                    "doc_language": LATEX_LANGUAGES[lang],
                    "title": state,
                    "year": year,
                    "footer_url": "https://ramiboutas.com",
                    "holidays_part1": holidays_part1,
                    "holidays_part2": holidays_part2,
                }

                # Article in md
                create_article(lang, state, year, country_code, context, md_table)

                # Listing
                listing_context = copy(context)
                listing_context.pop("footer_url")
                create_calendar(
                    lang, year, context, state=state, country_code=country_code
                )
                print(f"✔ Calendar {year} {state} {lang} created")


def create_article(lang, state, year, country_code, context, md_table):
    title = get_article_title(lang, state, year, country_code)
    path = Path(f"material/articles/{lang}/{TOPIC_SLUG}/{title}/body.md")
    path.parent.mkdir(exist_ok=True, parents=True)
    pdf_path = path.parent / f"{year}_{slugify(state)}.pdf"

    with open(pdf_path, "wb") as f:
        f.write(render_pdf("calendar.tex", context))

    content = md_table + "\n\n" + f"[{str(pdf_path.name)}]({pdf_path.name})"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def get_weekday_emoji(number):
    if number in [0, 4]:
        # very happy
        return random.choice(["😁", "🤭", "😎", "🎉", "🎊", "🙌", "🥳"])
    elif number in [5, 6]:
        # very sad
        return random.choice(["😢", "😞", "🙁", "😥"])
    else:
        # neutral
        return random.choice(["🎁", "🙂", "💚"])


def get_article_title(lang, state, year, country_code):
    country = TEXT_COUNTRIES[country_code][lang]
    if lang == "en":
        return f"Public holidays in {state} ({country}) for the year {year}"
    if lang == "es":
        return f"Días festivos en {state} ({country}) para el año {year}"
    if lang == "de":
        return f"Feiertage in {state} ({country}) für das Jahr {year}"
