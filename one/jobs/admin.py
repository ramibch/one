from django.contrib import admin

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    autocomplete_fields = ("company_locations", "recruiter")
    search_fields = ("title", "company__name", "recruiter__name", "extern_id")
    list_display = ("__str__", "recruiter", "source_url")
    list_filter = ("language",)
    readonly_fields = ("is_active", "expires_on")
