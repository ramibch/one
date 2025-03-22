from datetime import datetime

from django.db import models

from one.base.utils.abstracts import TranslatableModel

from .compile import render_pdf
from .values import LATEX_LANGUAGES


class TexHoliday:
    def __init__(self, date, title) -> None:
        self.date = date
        self.title = title

    def tex_date(self):
        return self.date.strftime("%Y-%m-%d")


class YearlyHolidayCalender(TranslatableModel):
    # https://holidays.readthedocs.io/en/latest/#
    year = models.SmallIntegerField()
    title = models.CharField(max_length=256)
    pdf = models.FileField(null=True)
    image = models.ImageField(null=True)

    def test_calendar(self):
        lang_code = "es"
        year = 2024

        holidays_part1 = [
            TexHoliday(datetime(year, 1, 1), "Neujahr"),
            TexHoliday(datetime(year, 4, 3), "Testiing"),
        ]
        holidays_part2 = [TexHoliday(datetime(year, 12, 3), "Testing1!!")]

        context = {
            "doc_language": LATEX_LANGUAGES[lang_code],
            "title": "My calendar title",
            "year": self.year,
            "footer_url": "https://ramiboutas.com",
            "holidays_part1": holidays_part1,
            "holidays_part2": holidays_part2,
        }
        pdf = render_pdf("calendars/calendar.tex", context)
        # TODO
        return pdf
