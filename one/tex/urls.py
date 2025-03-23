from django.conf import settings
from django.urls import path

from .feeds import YearlyHolidayCalenderPinFeed
from .views import YearlyHolidayCalenderView

pin_urlpatterns = [
    path(f"pins/yearly-calendars/{lang}", YearlyHolidayCalenderPinFeed(lang))
    for lang in settings.LANGUAGE_CODES
]


urlpatterns = [
    path(
        "cal/<int:year>/<str:country>/<str:subdiv>",
        YearlyHolidayCalenderView.as_view(),
        name="tex_yearly_holiday_subdiv_calendar",
    ),
    path(
        "cal/<int:year>/<str:country>",
        YearlyHolidayCalenderView.as_view(),
        name="tex_yearly_holiday_no_subdiv_calendar",
    ),
] + pin_urlpatterns
