from django.contrib import admin

from one.base.utils.admin import FORMFIELD_OVERRIDES_DICT

from .models import Company, CompanyLocation, Job, Person


class CompanyLocationInline(admin.TabularInline):
    model = CompanyLocation
    extra = 1
    autocomplete_fields = ("geo_info",)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("__str__", "website", "jobs_page_html_is_empty")
    search_fields = ("name", "website")
    inlines = [CompanyLocationInline]
    actions = ["reset_jobs_page_html"]

    @admin.action(description="🗑️ Reset html content of job list page")
    def reset_jobs_page_html(modeladmin, request, queryset):
        queryset.update(jobs_page_html=None)


@admin.register(CompanyLocation)
class CompanyLocationAdmin(admin.ModelAdmin):
    list_display = ("company", "geo_info")
    search_fields = ("geo_info__address", "company__name")
    autocomplete_fields = ("company", "geo_info")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ("full_name", "email")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    autocomplete_fields = ("company_locations", "recruiter", "company")
    search_fields = ("title", "company__name", "recruiter__name", "extern_id")
    list_display = ("__str__", "recruiter", "source_url")
    list_filter = ("language",)
    readonly_fields = ("is_active", "expires_on")
