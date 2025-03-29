from django.contrib import admin

from .models import EnglishQuizLection, YearlyHolidayCalender


class TexModelAdmin(admin.ModelAdmin):
    actions = ["render"]

    @admin.action(description="🔄 Render")
    def render(modeladmin, request, queryset):
        for obj in queryset:
            obj.render()


@admin.register(YearlyHolidayCalender)
class YearlyHolidayCalenderAdmin(TexModelAdmin):
    pass


@admin.register(EnglishQuizLection)
class EnglishQuizLectionAdmin(TexModelAdmin):
    pass
