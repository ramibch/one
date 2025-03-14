from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from one.base.utils.actions import translate_fields
from one.base.utils.admin import FORMFIELD_OVERRIDES_DICT

from .models import FAQ


@admin.register(FAQ)
class FAQAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("__str__", "question", "answer", "category")
    list_editable = ("category",)
    search_fields = ("question", "answer")
    actions = [translate_fields]
