from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Book, Chapter, ChapterFile


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    filter_horizontal = ("sites",)
    readonly_fields = ("name",)

    def has_delete_permission(self, request, obj=...):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Chapter)
class ChapterAdmin(TranslationAdmin):
    list_display = (
        "title",
        "folder_name",
        "subfolder_name",
        "created_on",
        "updated_on",
    )
    readonly_fields = (
        "title",
        "book",
        "folder_name",
        "subfolder_name",
        "body",
        "created_on",
        "updated_on",
    )
    list_filter = ("book", "folder_name", "created_on", "updated_on")
    search_fields = ("title", "folder_name", "subfolder_name", "body")

    def has_delete_permission(self, request, obj=...):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(ChapterFile)
class ChapterFileAdmin(admin.ModelAdmin):
    list_display = ("name", "chapter", "file")
    readonly_fields = ("name", "chapter", "file")

    def has_add_permission(self, request):
        return False
