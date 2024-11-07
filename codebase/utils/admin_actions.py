from django.contrib import admin
from modeltranslation.translator import translator

from ..utils.telegram import Bot
from .tasks import translate_null_field_from_a_queryset


def dummy_translate(from_lang, to_lang, text):
    return f"Dummy translation: {from_lang} -> {to_lang}."


@admin.action(description="🈂️ Translate empty fields from default language")
def translate_null_fields(modeladmin, request, queryset):
    Model = modeladmin.model

    if Model not in translator.get_registered_models():
        Bot.to_admin(f"{Model} is not registered for translation.")
        return

    translation_fields = translator.get_options_for_model(Model).get_field_names()

    translate_null_field_from_a_queryset(queryset, translation_fields)
