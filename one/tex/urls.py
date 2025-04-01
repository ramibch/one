from django.urls import path

from .views import YearlyHolidayCalenderView, temp_calendar

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
    # Avoid 404 (temp)
    path("public-holidays-in-<str:sd>-<str:c>-for-the-year-<int:y>", temp_calendar),
    path("feiertage-in-<str:sd>-<str:c>-fur-das-jahr-<int:y>", temp_calendar),
    path("dias-festivos-en-<str:sd>-<str:c>-para-el-ano-<int:y>", temp_calendar),
    path("public-holidays-in-<str:sd>-<str:c>-for-the-year-<int:y>/", temp_calendar),
    path("feiertage-in-<str:sd>-<str:c>-fur-das-jahr-<int:y>/", temp_calendar),
    path("dias-festivos-en-<str:sd>-<str:c>-para-el-ano-<int:y>/", temp_calendar),
]
