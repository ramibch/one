from django.urls import path

from .views import YearlyHolidayCalenderView

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
]
