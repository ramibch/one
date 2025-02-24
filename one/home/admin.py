from django.contrib import admin
from django.forms.widgets import CheckboxSelectMultiple
from modeltranslation.admin import TranslationAdmin

from one.base.utils.actions import translate_fields
from one.base.utils.admin import FORMFIELD_OVERRIDES_DICT

from ..base.utils.db import ChoiceArrayField
from .models import ArticlesSection, FAQsSection, HeroSection, Home


@admin.register(Home)
class HomeAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    actions = [translate_fields]
    list_display = ("__str__", "title", "site")


@admin.register(FAQsSection)
class FAQsSectionAdmin(TranslationAdmin):
    formfield_overrides = {ChoiceArrayField: {"widget": CheckboxSelectMultiple}}


@admin.register(ArticlesSection)
class ArticlesSectionAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    actions = [translate_fields]


@admin.register(HeroSection)
class HomeHeroAdmin(TranslationAdmin):
    list_display = ("headline", "cta_link", "image")
    list_editable = ("cta_link", "image")
    list_filter = ("home",)
    actions = [translate_fields]
