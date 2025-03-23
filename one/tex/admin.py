from django.contrib import admin

from one.base.utils.admin import TranslatableModelAdmin

from .models import YearlyHolidayCalender


class TODOYearlyHolidayCalenderAdmin(TranslatableModelAdmin):
    pass


@admin.register(YearlyHolidayCalender)
class YearlyHolidayCalenderAdmin(admin.ModelAdmin):
    actions = ["render"]

    @admin.action(description="🔄 Render calendar")
    def render(modeladmin, request, queryset):
        for obj in queryset:
            obj.render()
