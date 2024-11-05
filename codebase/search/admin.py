from django.contrib import admin

from .models import SearchTerm


@admin.register(SearchTerm)
class SearchTermAdmin(admin.ModelAdmin):
    list_display = ("query", "user", "country_code", "created_on")
    readonly_fields = ("query", "user", "country_code", "created_on")
    list_filter = ("user", "country_code", "created_on")
