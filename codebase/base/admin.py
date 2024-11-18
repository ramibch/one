from django.contrib import admin
from django.db.migrations.recorder import MigrationRecorder
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from huey.contrib.djhuey import HUEY
from modeltranslation.admin import TranslationAdmin

from ..articles.tasks import trigger_sync_articles
from ..pages.tasks import trigger_sync_pages
from ..utils.actions import translation_actions
from ..utils.admin import FORMFIELD_OVERRIDES_DICT
from .models import ArticlesFolder, ExtendedSite, PagesFolder, Traffic


@admin.register(ArticlesFolder)
@admin.register(PagesFolder)
class ArticleFolderAdmin(admin.ModelAdmin):
    pass


@admin.register(ExtendedSite)
class ExtendedSiteAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("__str__", "domain", "name")
    search_fields = ("domain", "name")
    readonly_fields = ("last_huey_flush",)
    list_editable = ("domain", "name")
    actions = translation_actions + ["flush_huey", "sync_articles", "sync_pages"]

    fieldsets = (
        (
            _("Site fields"),
            {"fields": ("domain", "name")},
        ),
        (
            _("Management"),
            {"fields": ("remarks", "last_huey_flush", "allow_field_translation")},
        ),
        (
            _("Submodules"),
            {"fields": ("article_folders", "page_folders")},
        ),
        (
            _("Brand"),
            {"fields": ("emoji", "emoji_in_brand")},
        ),
        (
            _("Defaults"),
            {"fields": ("default_page_title", "default_page_description", "default_page_keywords")},
        ),
        (
            _("Appearance and design"),
            {
                "fields": (
                    "change_theme_light_in_navbar",
                    "change_language_in_navbar",
                    "change_theme_light_in_footer",
                    "change_language_in_footer",
                )
            },
        ),
    )

    @admin.action(description="🗑️ Flush Huey | revoke tasks")
    def flush_huey(modeladmin, request, queryset):
        HUEY.flush()
        queryset.update(last_huey_flush=now())

    @admin.action(description="🔄 Sync articles")
    def sync_articles(modeladmin, request, queryset):
        trigger_sync_articles(queryset)

    @admin.action(description="🔄 Sync pages")
    def sync_pages(modeladmin, request, queryset):
        trigger_sync_pages(queryset)


@admin.register(MigrationRecorder.Migration)
class MigrationRecorderAdmin(admin.ModelAdmin):
    list_display = ("name", "app", "applied")
    list_filter = ("app", "applied")


@admin.register(Traffic)
class TrafficAdmin(admin.ModelAdmin):
    list_display = ("__str__", "request_path", "response_code", "request_method", "request_user")
    list_filter = ("time", "request_site", "request_method", "response_code")
    readonly_fields = (
        "request_GET",
        "request_GET_ref",
        "request_POST",
        "request_path",
        "request_headers",
        "request_country_code",
        "response_headers",
        "response_code",
        "request_method",
        "request_user",
        "request_site",
        "time",
    )
