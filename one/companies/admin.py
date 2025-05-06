from django.contrib import admin

from one.base.utils.admin import FORMFIELD_OVERRIDES_DICT

from .models import Company, CompanyLocation, Person


class CompanyLocationInline(admin.TabularInline):
    model = CompanyLocation
    extra = 1
    autocomplete_fields = ("geo_info",)


@admin.register(CompanyLocation)
class CompanyLocationAdmin(admin.ModelAdmin):
    list_display = ("company", "geo_info")
    search_fields = ("geo_info__address", "company__name")
    autocomplete_fields = ("company", "geo_info")


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("__str__", "website")
    list_filter = ("application_methods",)
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    search_fields = ("name", "website")
    inlines = [CompanyLocationInline]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ("full_name", "email")
