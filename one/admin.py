from django.contrib import admin
from django.contrib.admin import StackedInline, TabularInline
from django.contrib.gis.admin.options import GeoModelAdminMixin  # type: ignore
from django.db import models
from django.forms.widgets import CheckboxSelectMultiple
from modeltranslation.admin import (
    TranslationAdmin,
    TranslationTabularInline,
)
from modeltranslation.translator import translator

from one.db import ChoiceArrayField

from .base.tasks import translate_modeltranslation_objects
from .bot import Bot

FORMFIELD_OVERRIDES = {
    models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    ChoiceArrayField: {"widget": CheckboxSelectMultiple},
}


class OneModelAdmin(admin.ModelAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES


class OneStackedInline(admin.StackedInline):
    formfield_overrides = FORMFIELD_OVERRIDES


class OneTabularInline(admin.TabularInline):
    formfield_overrides = FORMFIELD_OVERRIDES


class OneTranslatableModelAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES

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

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions["translate_fields"] = (
            self.translate_fields,
            "translate_fields",
            self.translate_fields.short_description,
        )
        return actions


class OneTranslationStackedInline(TranslationTabularInline):
    formfield_overrides = FORMFIELD_OVERRIDES


class OneTranslationTabularInline(TranslationTabularInline):
    formfield_overrides = FORMFIELD_OVERRIDES


class TranslatableGISModelAdmin(GeoModelAdminMixin, OneTranslatableModelAdmin):
    pass


class GISStackedInline(GeoModelAdminMixin, StackedInline):
    pass


class GISTabularInline(GeoModelAdminMixin, TabularInline):
    pass
