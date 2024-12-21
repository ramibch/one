from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Page, PageParentFolder


@admin.register(PageParentFolder)
class PageParentFolderAdmin(admin.ModelAdmin):
    pass

    def has_delete_permission(self, request, obj=...):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Page)
class PageAdmin(TranslationAdmin):
    list_display = (
        "title",
        "folder_name",
        "subfolder_name",
        "created_on",
        "updated_on",
    )
    readonly_fields = (
        "title",
        "folder_name",
        "subfolder_name",
        "body",
        "created_on",
        "updated_on",
    )
    list_filter = ("subfolder_name", "created_on", "updated_on")
    search_fields = ("title", "folder_name", "subfolder_name", "body")

    def has_delete_permission(self, request, obj=...):
        return False

    def has_add_permission(self, request):
        return False
