from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

from ..utils.actions import translation_actions
from .models import Hero, HeroCTA, HomePage


class HeroInline(TranslationStackedInline):
    model = Hero
    extra = 1


@admin.register(HomePage)
class HomePageAdmin(TranslationAdmin):
    actions = translation_actions
    inlines = (HeroInline,)


@admin.register(Hero)
class HeroAdmin(TranslationAdmin):
    list_display = ("headline", "cta", "image", "is_active", "allow_field_translation")
    list_editable = ("is_active", "cta", "image", "allow_field_translation")
    list_filter = ("homepage", "homepage__site", "is_active", "allow_field_translation")
    actions = translation_actions


@admin.register(HeroCTA)
class HeroCTAAdmin(TranslationAdmin):
    actions = translation_actions
