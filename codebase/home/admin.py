from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

from ..utils.actions import translation_actions
from .models import HeroSection, HomePage


class HomePageHeroInline(TranslationStackedInline):
    model = HeroSection
    extra = 1


@admin.register(HomePage)
class HomeAdmin(TranslationAdmin):

    inlines = (HomePageHeroInline,)
    actions = translation_actions


@admin.register(HeroSection)
class HomePageHeroAdmin(TranslationAdmin):
    list_display = ("headline", "cta_link", "image", "is_active", "allow_field_translation")
    list_editable = ("is_active", "cta_link", "image", "allow_field_translation")
    list_filter = ("homepage", "homepage__site", "is_active", "allow_field_translation")
    actions = translation_actions
