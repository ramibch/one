from django.contrib import admin
from django.db import models
from django.forms.widgets import CheckboxSelectMultiple
from django.urls import reverse
from modeltranslation.admin import TranslationAdmin
from modeltranslation.translator import translator

from one.base.utils.db import ChoiceArrayField

from ..tasks import translate_modeltranslation_objects
from .telegram import Bot

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


def get_edit_object_admin_url(obj) -> str:
    return reverse(
        f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change", args=(obj.pk,)
    )
