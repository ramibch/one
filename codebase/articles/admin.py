from django.contrib import admin

from .models import Article, ArticleFile


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "featured", "folder", "subfolder", "created_on", "updated_on")
    list_editable = ("featured",)
    readonly_fields = ("title", "folder", "subfolder", "body", "created_on", "updated_on")
    list_filter = ("folder", "created_on", "updated_on")


@admin.register(ArticleFile)
class ArticleFileAdmin(admin.ModelAdmin):
    list_display = ("name", "article", "file")
    readonly_fields = ("name", "article", "file")
