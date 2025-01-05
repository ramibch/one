from copy import deepcopy

from django.utils.text import slugify

from ..listings import Listing, validate_keywords
from ..texts import (
    TEXT_A4_FORMAT_CALENDAR,
    TEXT_CALENDAR,
    TEXT_CALENDAR_PRINTABLE,
    TEXT_COUNTRIES,
    TEXT_FULLYEAR_CALENDAR,
    TEXT_MONTHLY_PLANNER,
    TEXT_SUMMARY_FOR_CALENDARS,
    TEXT_WALL_CALENDAR,
    TEXTLIST_COMMOM_CALENDAR_TAGS,
)


def get_extra_listing_keywords(lang):
    keywords = (
        TEXT_FULLYEAR_CALENDAR[lang],
        TEXT_CALENDAR_PRINTABLE[lang],
        TEXT_A4_FORMAT_CALENDAR[lang],
        TEXT_WALL_CALENDAR[lang],
        TEXT_MONTHLY_PLANNER[lang],
    )
    return ", ".join(keywords)


def get_tags(lang, year, state=None, country_code=None):
    tags = deepcopy(TEXTLIST_COMMOM_CALENDAR_TAGS[lang])
    tags.append(str(year))
    if state:
        tags.append(state)
    if country_code:
        tags.append(TEXT_COUNTRIES[country_code][lang])
    return tags


def get_main_listing_keywords(lang, year, state=None, country_code=None):
    out = TEXT_CALENDAR[lang] + " " + str(year)
    if state:
        out += " " + state
    if country_code:
        out += " - " + TEXT_COUNTRIES[country_code][lang]
    return out


def get_summary(lang, year, state=None, country_code=None):
    # TODO: use the params
    return TEXT_SUMMARY_FOR_CALENDARS[lang]


def create_calendar(
    lang: str,
    year: int,
    context: dict,
    template_name: str = "calendar.tex",
    state: str = None,
    country_code: str = None,
):
    if "year" not in context:
        context["year"] = year

    # title
    main_keywords = get_main_listing_keywords(
        lang, year, state=state, country_code=country_code
    )
    extra_keywords = get_extra_listing_keywords(lang)
    keywords = validate_keywords(f"{main_keywords}, {extra_keywords}")
    # dirname and filename
    if state is None:
        dirname = f"{year}_{TEXT_CALENDAR[lang]}"
        filename = f"{year}_{TEXT_CALENDAR[lang]}.pdf"
    else:
        dirname = f"{year}_{TEXT_CALENDAR[lang]}_{slugify(state)}_{lang}"
        filename = f"{year}_{slugify(state)}.pdf"

    # Listing
    listing = Listing.objects.get_or_create(
        keywords=keywords,
        title=main_keywords,
        dirname=dirname,
        listing_type="calendar",
        price=1.49,
        lang=lang,
        tags=get_tags(lang, year, state=state, country_code=country_code),
    )
    # summary
    summary = get_summary(lang, year, state=state, country_code=country_code)
    listing.write_summary(summary)
    # pdf
    listing.render_latex_file(template_name, filename, context)
    return listing
