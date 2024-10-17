from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "folder", "created_on", "updated_on")
    list_filter = ("topic", "created_on", "updated_on")
