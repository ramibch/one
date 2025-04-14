from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from one.base.utils.admin import FORMFIELD_OVERRIDES_DICT

from .models import Article, ArticleFile, MainTopic


@admin.register(MainTopic)
class MainTopicAdmin(admin.ModelAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("name", "present_in_filesystem")
    # readonly_fields = ("name", "present_in_filesystem")
    list_filter = ("present_in_filesystem",)


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("__str__", "featured", "created_on", "updated_on")

    list_filter = ("main_topic", "folder_name", "created_on", "updated_on")
    search_fields = ("title", "folder_name", "subfolder_name", "body")

    actions = ["mark_as_featured", "mark_as_not_featured"]

    @admin.action(description="✅ Mark as featured")
    def mark_as_featured(modeladmin, request, queryset):
        queryset.update(featured=True)

    @admin.action(description="◻️ Mark as not featured")
    def mark_as_not_featured(modeladmin, request, queryset):
        queryset.update(featured=False)


@admin.register(ArticleFile)
class ArticleFileAdmin(admin.ModelAdmin):
    list_display = ("name", "article", "file")
    readonly_fields = ("name", "article", "file")

    def has_add_permission(self, request):
        return False
