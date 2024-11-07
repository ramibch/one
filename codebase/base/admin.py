from django.contrib import admin
from django.db.migrations.recorder import MigrationRecorder
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from huey.contrib.djhuey import HUEY
from modeltranslation.admin import TranslationAdmin

from ..utils.admin_actions import translate_null_fields
from .models import ExtendedSite


@admin.register(MigrationRecorder.Migration)
class MigrationRecorderAdmin(admin.ModelAdmin):
    list_display = ("name", "app", "applied")
    list_filter = ("app", "applied")
    actions = ("set_applied_now",)

    @admin.action(description="Set applied now | ⚠️ You must know what you are doing!")
    def set_applied_now(modeladmin, request, queryset):
        queryset.update(applied=now())


@admin.register(ExtendedSite)
class ExtendedSiteAdmin(TranslationAdmin):
    list_display = ("__str__", "domain", "name")
    search_fields = ("domain", "name")
    readonly_fields = ("last_huey_flush",)
    list_editable = ("domain", "name")
    actions = ["flush_huey", translate_null_fields]

    fieldsets = (
        (
            _("Site fields"),
            {"fields": ("domain", "name")},
        ),
        (
            _("Management"),
            {"fields": ("remarks", "last_huey_flush")},
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

    @admin.action(description="🔄 Flush Huey | revoke tasks")
    def flush_huey(modeladmin, request, queryset):
        HUEY.flush()
        queryset.update(last_huey_flush=now())
