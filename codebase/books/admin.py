from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Book, Chapter, ChapterFile


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


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


@admin.register(ChapterFile)
class ChapterFileAdmin(admin.ModelAdmin):
    list_display = ("name", "chapter", "file")
    readonly_fields = ("name", "chapter", "file")
