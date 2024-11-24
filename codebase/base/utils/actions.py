from django.contrib import admin
from modeltranslation.translator import translator

from ..tasks import translate_modeltranslation_objects
from .telegram import Bot


@admin.action(description="🈂️ Translate fields from default language")
def translate_from_default_language(modeladmin, request, queryset):
    """
    Translate fields of a QuerySet from the default language.
    """
    Model = modeladmin.model

    if Model not in translator.get_registered_models():
        Bot.to_admin(f"{Model} is not registered for translation.")
        return

    field_names = translator.get_options_for_model(Model).get_field_names()
    translate_modeltranslation_objects(queryset, field_names)


@admin.action(description="☑️ Allow field translation")
def allow_translation_for_qs(modeladmin, request, queryset):
    queryset.update(allow_translation=True)


@admin.action(description="⏹️ Disallow field translation")
def disallow_translation_for_qs(modeladmin, request, queryset):
    queryset.update(allow_translation=False)


translation_actions = [
    translate_from_default_language,
    allow_translation_for_qs,
    disallow_translation_for_qs,
]
