from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Article, ArticleFile, ArticleParentFolder


@admin.register(ArticleParentFolder)
class ArticlesSubmoduleAdmin(admin.ModelAdmin):
    filter_horizontal = ("sites",)
    readonly_fields = ("name",)

    def has_delete_permission(self, request, obj=...):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    list_display = (
        "title",
        "folder_name",
        "subfolder_name",
        "created_on",
        "updated_on",
    )
    readonly_fields = (
        "title",
        "parent_folder",
        "folder_name",
        "subfolder_name",
        "body",
        "created_on",
        "updated_on",
    )
    list_filter = ("parent_folder", "folder_name", "created_on", "updated_on")
    search_fields = ("title", "folder_name", "subfolder_name", "body")

    def has_delete_permission(self, request, obj=...):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(ArticleFile)
class ArticleFileAdmin(admin.ModelAdmin):
    list_display = ("name", "article", "file")
    readonly_fields = ("name", "article", "file")

    def has_add_permission(self, request):
        return False
