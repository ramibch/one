from django.contrib import admin

from one.base.utils.admin import TranslatableModelAdmin

from .models import YearlyHolidayCalender


class TODOYearlyHolidayCalenderAdmin(TranslatableModelAdmin):
    pass


@admin.register(YearlyHolidayCalender)
class YearlyHolidayCalenderAdmin(admin.ModelAdmin):
    pass
