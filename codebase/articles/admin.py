from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Article, ArticleFile


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    list_display = ("title", "featured", "folder", "subfolder", "created_on", "updated_on")
    list_editable = ("featured",)
    readonly_fields = ("title", "sites", "submodule_folder", "folder", "subfolder", "body", "created_on", "updated_on")
    list_filter = ("folder", "created_on", "updated_on")
    search_fields = ("title", "folder", "subfolder", "body")


@admin.register(ArticleFile)
class ArticleFileAdmin(admin.ModelAdmin):
    list_display = ("name", "parent_page", "file")
    readonly_fields = ("name", "parent_page", "file")
