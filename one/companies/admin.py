from django.contrib import admin

from one.admin import FORMFIELD_OVERRIDES_DICT

from .models import Company, CompanyLocation, Job, Person
from .tasks import scrape_company_pages, scrape_job_detail_pages


class CompanyLocationInline(admin.TabularInline):
    model = CompanyLocation
    extra = 1
    autocomplete_fields = ("geoinfo",)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("__str__", "website", "jobs_page_html_is_empty")
    search_fields = ("name", "website")
    list_filter = ("jobs_scrape_ready",)
    actions = ["reset_jobs_page_html", "scrape_pages"]
    inlines = [CompanyLocationInline]

    @admin.action(description="🗑️ Reset html content of job list page")
    def reset_jobs_page_html(modeladmin, request, queryset):
        queryset.update(jobs_page_html=None)

    @admin.action(description="🧐 Scrape company pages")
    def scrape_pages(modeladmin, request, queryset):
        scrape_company_pages(queryset)


@admin.register(CompanyLocation)
class CompanyLocationAdmin(admin.ModelAdmin):
    list_display = ("company", "geoinfo")
    search_fields = ("local_name",)
    autocomplete_fields = ("company", "geoinfo")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ("full_name", "email")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    autocomplete_fields = ("company_locations", "recruiter", "company")
    search_fields = ("title", "body")
    list_display = ("__str__", "recruiter", "source_url")
    list_filter = ("language",)
    readonly_fields = ("is_active", "expires_on")

    actions = ["scrape_pages"]

    @admin.action(description="🧐 Scrape job pages")
    def scrape_pages(modeladmin, request, queryset):
        scrape_job_detail_pages(queryset)
