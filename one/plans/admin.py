from django.contrib import admin

from one.base.utils.admin import TranslatableModelAdmin

from .models import Plan


@admin.register(Plan)
class PlanAdmin(TranslatableModelAdmin):
    search_fields = ("title", "description")
