from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Article, ArticleFile, ArticleParentFolder


@admin.register(ArticleParentFolder)
class ArticlesSubmoduleAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    list_display = ("title", "folder", "subfolder", "created_on", "updated_on")
    readonly_fields = (
        "title",
        "parent",
        "folder",
        "subfolder",
        "body",
        "created_on",
        "updated_on",
    )
    list_filter = ("parent", "folder", "created_on", "updated_on")
    search_fields = ("title", "folder", "subfolder", "body")


@admin.register(ArticleFile)
class ArticleFileAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "file")
    readonly_fields = ("name", "parent", "file")
