from django.contrib import admin
from modeltranslation.translator import translator

from ..tasks import translate_modeltranslation_objects
from .telegram import Bot


@admin.action(description="🈂️ Translate fields from default language")
def translate_fields(modeladmin, request, queryset):
    """
    Translate fields of a QuerySet from the default language.
    """
    Model = modeladmin.model

    if Model not in translator.get_registered_models():
        Bot.to_admin(f"{Model} is not registered for translation.")
        return

    field_names = translator.get_options_for_model(Model).get_field_names()
    translate_modeltranslation_objects(queryset, field_names)
