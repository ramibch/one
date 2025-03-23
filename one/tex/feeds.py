from django.contrib.syndication.views import Feed
from django.utils import timezone
from django.utils.translation import activate
from django.utils.translation import gettext_lazy as _

from one import settings

from .models import YearlyHolidayCalender


class YearlyHolidayCalenderPinFeed(Feed):
    DAYS = 90
    title = _("List of calendars")
    link = "/"
    description = _("Last calendars published in my sites")
    item_enclosure_mime_type = "image/png"

    def __init__(self, lang: str) -> None:
        assert lang in settings.LANGUAGE_CODES
        activate(lang)
        self.lang = lang
        super().__init__()

    def items(self):
        past = timezone.now() - timezone.timedelta(days=self.DAYS)
        return YearlyHolidayCalender.objects.exclude(pdf="", image="").filter(
            created_on__gte=past, lang=self.lang
        )

    def item_title(self, item: YearlyHolidayCalender):
        return f"{str(_('Calendar'))} {item.year} | {item.title}"

    def item_description(self, item: YearlyHolidayCalender):
        return "\n".join(
            f"{d.strftime('%Y-%m-%d')} - {n}" for d, n in item.country_holidays
        )

    def item_lastupdated(self, item: YearlyHolidayCalender):
        return item.updated_on

    def item_enclosure_url(self, item: YearlyHolidayCalender):
        return item.image.url

    def item_enclosure_length(self, item: YearlyHolidayCalender):
        return item.image.size
