import holidays
from django.utils.timezone import now
from huey import crontab
from huey.contrib import djhuey as huey

from one.choices import Countries
from one.quiz.models import Lection

from .models import EnglishQuizLection, YearlyHolidayCalender
from .values import TEX_LANGUAGE_MAPPING

# Calendars


@huey.db_periodic_task(crontab(day="5", hour="5", minute="55"))
def create_yearly_holiday_calendars():
    """Create calendar objects"""
    this_year = now().year

    year_list = list(range(this_year - 1, this_year + 3))
    objs = []

    # Fetch existing records in bulk
    existing_records = list(
        set(
            YearlyHolidayCalender.objects.filter(year__in=year_list).values_list(
                "year", "country", "subdiv", "lang"
            )
        )
    )

    for country_code in Countries.values:
        country_holidays = getattr(holidays, country_code, None)
        if not country_holidays:
            continue

        country_langs = {x.split("_")[0] for x in country_holidays.supported_languages}
        default_language = (country_holidays.default_language or "").split("_")[0]

        lang = (
            default_language
            if default_language in TEX_LANGUAGE_MAPPING
            else next(
                (lng for lng in country_langs if lng in TEX_LANGUAGE_MAPPING),
                None,
            )
        )

        if lang is None:
            continue

        for year in year_list:
            for subdiv in [None] + list(country_holidays.subdivisions):
                if (year, country_code, subdiv, lang) not in existing_records:
                    objs.append(
                        YearlyHolidayCalender(
                            year=year, country=country_code, subdiv=subdiv, lang=lang
                        )
                    )

    if objs:
        YearlyHolidayCalender.objects.bulk_create(objs)


@huey.db_periodic_task(crontab(day="4", hour="4", minute="44"))
def remove_old_yearly_holiday_calendars():
    """Let us forget the past and remove old calendars..."""

    YearlyHolidayCalender.objects.filter(year__lt=now().year - 1).delete()


@huey.db_periodic_task(crontab(minute="15"))
def render_yearly_calendars():
    for c in YearlyHolidayCalender.objects.filter(pdf="").order_by("?")[:20]:
        c.render()


# English Quiz Lection objects


@huey.db_periodic_task(crontab(hour="7", minute="34"))
def create_english_quiz_lection_objects():
    lections = Lection.objects.filter(englishquizlection__isnull=True)
    objs = [EnglishQuizLection(lection=lec) for lec in lections]
    EnglishQuizLection.objects.bulk_create(objs)


@huey.db_periodic_task(crontab(minute="45"))
def render_english_quiz_lections():
    for c in EnglishQuizLection.objects.filter(pdf="").order_by("?")[:20]:
        c.render()
