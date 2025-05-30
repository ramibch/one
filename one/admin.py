from django.contrib import admin
from django.db import models
from django.forms.widgets import CheckboxSelectMultiple
from modeltranslation.admin import TranslationAdmin
from modeltranslation.translator import translator

from one.db import ChoiceArrayField

from .base.tasks import translate_modeltranslation_objects
from .bot import Bot

FORMFIELD_OVERRIDES_DICT = {
    models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    ChoiceArrayField: {"widget": CheckboxSelectMultiple},
}


class TranslatableModelAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    actions = ["translate_fields"]

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
