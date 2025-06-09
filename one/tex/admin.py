from django.contrib import admin

from one.admin import OneModelAdmin

from .models import EnglishQuizLection, YearlyHolidayCalender


@admin.register(YearlyHolidayCalender)
class YearlyHolidayCalenderAdmin(OneModelAdmin):
    list_filter = ("year", "lang", "country")
    list_display = ("id", "year", "country", "subdiv", "lang")
    search_fields = ("id", "year", "country")
    actions = ["render_calendars"]

    @admin.action(description="🔄 Render calendars")
    def render_calendars(modeladmin, request, queryset):
        for obj in queryset:
            obj.render_calendar()


@admin.register(EnglishQuizLection)
class EnglishQuizLectionAdmin(OneModelAdmin):
    actions = ["render_lections"]

    @admin.action(description="🔄 Render lections")
    def render_lections(modeladmin, request, queryset):
        for obj in queryset:
            obj.render_lection()
