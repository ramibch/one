from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from one.base.utils.admin import FORMFIELD_OVERRIDES_DICT

from .models import Article, ArticleFile, ArticleParentFolder


@admin.register(ArticleParentFolder)
class ArticlesSubmoduleAdmin(admin.ModelAdmin):
    readonly_fields = ("name",)

    def has_delete_permission(self, request, obj=...):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("__str__", "created_on", "updated_on")
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

    actions = ["mark_as_featured", "mark_as_not_featured"]

    def has_delete_permission(self, request, obj=...):
        return False

    def has_add_permission(self, request):
        return False

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
