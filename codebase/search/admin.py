from django.contrib import admin

from .models import SearchTerm


@admin.register(SearchTerm)
class SearchTermAdmin(admin.ModelAdmin):
    list_display = ("query", "site", "user", "country_code", "created_on")
    readonly_fields = ("query", "site", "user", "country_code", "created_on")
    list_filter = ("site", "user", "country_code", "created_on")
    list_display_links = ("site", "user")
