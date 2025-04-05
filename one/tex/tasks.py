import holidays
from django.conf import settings
from django.utils import timezone
from huey import crontab
from huey.contrib import djhuey as huey

from one.quiz.models import Lection

from .models import EnglishQuizLection, YearlyHolidayCalender
from .values import LATEX_LANGUAGES

THIS_YEAR = timezone.now().year
LAST_YEAR = THIS_YEAR - 1
YEARS = list(range(LAST_YEAR, THIS_YEAR + 3))


# Calendars


# @huey.db_periodic_task(crontab(day="5", hour="5", minute="55"))
def create_yearly_holiday_calendars():
    """Create calendar objects"""
    objs = []

    # Fetch existing records in bulk
    existing_records = list(
        set(
            YearlyHolidayCalender.objects.filter(year__in=YEARS).values_list(
                "year", "country", "subdiv", "lang"
            )
        )
    )

    for country_code, _ in settings.COUNTRIES:
        country_holidays = getattr(holidays, country_code, None)
        if not country_holidays:
            continue

        country_langs = {x.split("_")[0] for x in country_holidays.supported_languages}
        default_language = (country_holidays.default_language or "").split("_")[0]

        lang = (
            default_language
            if default_language in LATEX_LANGUAGES
            else next((lng for lng in country_langs if lng in LATEX_LANGUAGES), None)
        )

        if lang is None:
            continue

        for year in YEARS:
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
    YearlyHolidayCalender.objects.filter(year__lt=LAST_YEAR).delete()


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
