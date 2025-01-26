from django.contrib import admin
from django.contrib.sessions.models import Session
from django.db.migrations.recorder import MigrationRecorder
from modeltranslation.admin import TranslationAdmin

from .models import Topic
from .utils.actions import translate_fields


@admin.register(MigrationRecorder.Migration)
class MigrationRecorderAdmin(admin.ModelAdmin):
    list_display = ("name", "app", "applied")
    list_filter = ("app", "applied")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("session_key", "expire_date")
    list_filter = ("expire_date",)
    readonly_fields = ("session_key", "session_data", "expire_date")


@admin.register(Topic)
class TopicAdmin(TranslationAdmin):
    actions = [translate_fields]
