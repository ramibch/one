from django.contrib import admin
from django.db.migrations.recorder import MigrationRecorder
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from huey.contrib.djhuey import HUEY
from modeltranslation.admin import TranslationAdmin

from ..utils.actions import translation_actions
from .models import FAQ


@admin.register(FAQ)
class FAQAdmin(TranslationAdmin):
    list_display = ("__str__", "question", "answer", "category")
    list_editable = ("category",)
    search_fields = ("question", "answer")
    actions = translation_actions
