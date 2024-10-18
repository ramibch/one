from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "folder", "subfolder", "created_on", "updated_on")
    list_filter = ("folder", "created_on", "updated_on")
