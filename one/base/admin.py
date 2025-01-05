from django.contrib import admin
from django.db.migrations.recorder import MigrationRecorder
from modeltranslation.admin import TranslationAdmin

from .models import Topic
from .utils.actions import translation_actions


@admin.register(MigrationRecorder.Migration)
class MigrationRecorderAdmin(admin.ModelAdmin):
    list_display = ("name", "app", "applied")
    list_filter = ("app", "applied")


@admin.register(Topic)
class TopicAdmin(TranslationAdmin):
    actions = translation_actions
