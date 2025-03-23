import holidays
from django.conf import settings
from django.utils import timezone
from huey import crontab
from huey.contrib import djhuey as huey

from .models import YearlyHolidayCalender as Calendar
from .values import LATEX_LANGUAGES


@huey.db_periodic_task(crontab(day="5", hour="5", minute="55"))
def create_yearly_holiday_calendars():
    objs = []
    this_year = timezone.now().year
    years = list(range(this_year, this_year + 3))
    for country_info in settings.COUNTRIES:
        country_code = country_info[0]
        if not hasattr(holidays, country_code):
            continue
        country_holidays = getattr(holidays, country_code)

        country_langs = [x.split("_")[0] for x in country_holidays.supported_languages]

        default_language = (country_holidays.default_language or "").split("_")[0]

        if default_language in LATEX_LANGUAGES:
            lang = default_language
        else:
            common_langs = list(set(country_langs) & set(LATEX_LANGUAGES.keys()))
            lang = common_langs[0] if common_langs else None

        if lang is None:
            continue

        subdivision_aliases = list(country_holidays.get_subdivision_aliases().values())

        if len(subdivision_aliases) == 0:
            subdivisions = country_holidays.subdivisions
        elif subdivision_aliases[0]:
            subdivisions = (" ".join(item) for item in subdivision_aliases)
        else:
            subdivisions = country_holidays.subdivisions

        for year in years:
            objs.append(
                Calendar(year=year, country=country_code, subdiv=None, lang=lang)
            )
            for subdiv in subdivisions:
                objs.append(
                    Calendar(year=year, country=country_code, subdiv=subdiv, lang=lang)
                )

    Calendar.objects.bulk_create(objs, ignore_conflicts=True)


@huey.db_periodic_task(crontab(minute="15"))
def render_yearly_calendars():
    for c in Calendar.objects.filter(pdf="")[:10]:
        c.render()
