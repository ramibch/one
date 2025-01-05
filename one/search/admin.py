from django.contrib import admin

from .models import SearchTerm


@admin.register(SearchTerm)
class SearchTermAdmin(admin.ModelAdmin):
    list_display = ("query", "site", "user", "client", "created_on")
    readonly_fields = ("query", "site", "user", "client", "created_on")
    list_filter = ("site", "user", "client", "created_on")
    list_display_links = ("site", "user")

    def has_add_permission(self, request):
        return False
