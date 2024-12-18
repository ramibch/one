from django.contrib import admin
from django.db.migrations.recorder import MigrationRecorder
from modeltranslation.admin import TranslationAdmin

from .models import Language, Topic, Traffic
from .utils.actions import translation_actions


@admin.register(MigrationRecorder.Migration)
class MigrationRecorderAdmin(admin.ModelAdmin):
    list_display = ("name", "app", "applied")
    list_filter = ("app", "applied")


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(Topic)
class TopicAdmin(TranslationAdmin):
    actions = translation_actions


@admin.register(Traffic)
class TrafficAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "request_path",
        "response_status_code",
        "request_method",
        "user",
    )
    list_filter = (
        "request_path",
        "site",
        "response_status_code",
        "request_method",
        "time",
    )
    readonly_fields = (
        "request_GET",
        "request_GET_ref",
        "request_POST",
        "request_path",
        "request_headers",
        "request_country_code",
        "response_headers",
        "response_status_code",
        "request_method",
        "user",
        "site",
        "time",
    )
