from django.contrib import admin

from one.admin import OneTranslatableModelAdmin

from .models import Plan


@admin.register(Plan)
class PlanAdmin(OneTranslatableModelAdmin):
    search_fields = ("title", "description")
