from django.contrib import admin
from django.db.migrations.recorder import MigrationRecorder
from modeltranslation.admin import TranslationAdmin

from .models import Topic, Traffic
from .utils.actions import translation_actions


@admin.register(MigrationRecorder.Migration)
class MigrationRecorderAdmin(admin.ModelAdmin):
    list_display = ("name", "app", "applied")
    list_filter = ("app", "applied")


@admin.register(Topic)
class TopicAdmin(TranslationAdmin):
    actions = translation_actions


@admin.register(Traffic)
class TrafficAdmin(admin.ModelAdmin):
    list_display = ("__str__", "path", "status_code", "method", "user")
    list_filter = ("path", "site", "status_code", "method", "time")
    readonly_fields = (
        "get",
        "ref",
        "post",
        "path",
        "headers",
        "country_code",
        "headers",
        "status_code",
        "method",
        "user",
        "site",
        "time",
    )
