from django.contrib import admin

from one.base.utils.admin import FORMFIELD_OVERRIDES_DICT

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    autocomplete_fields = ("company_location", "recruiter")
    search_fields = ("title", "company__name", "recruiter__name", "extern_id")
    list_display = ("__str__", "company_location", "recruiter", "source_url")
    list_filter = ("language",)
    readonly_fields = ("is_active", "expires_on")
