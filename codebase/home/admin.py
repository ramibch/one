from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from ..utils.actions import translation_actions
from ..utils.admin import FORMFIELD_OVERRIDES_DICT
from .models import HeroSection, HomePage


@admin.register(HomePage)
class HomePageAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    actions = translation_actions
    list_display = ("title",)


@admin.register(HeroSection)
class HomePageHeroAdmin(TranslationAdmin):
    list_display = ("headline", "cta_link", "image", "is_active", "allow_translation")
    list_editable = ("is_active", "cta_link", "image", "allow_translation")
    list_filter = ("homepage", "homepage__sites", "is_active", "allow_translation")
    actions = translation_actions
