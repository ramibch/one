from django.contrib import admin
from django.forms.widgets import CheckboxSelectMultiple
from modeltranslation.admin import TranslationAdmin

from one.base.utils.actions import translation_actions
from one.base.utils.admin import FORMFIELD_OVERRIDES_DICT

from ..base.utils.db_fields import ChoiceArrayField
from .models import ArticlesSection, FAQsSection, HeroSection, Home


@admin.register(Home)
class HomeAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    actions = translation_actions
    list_display = ("__str__", "title", "site")


@admin.register(FAQsSection)
class FAQsSectionAdmin(TranslationAdmin):
    filter_horizontal = ("faqs",)
    formfield_overrides = {ChoiceArrayField: {"widget": CheckboxSelectMultiple}}


@admin.register(ArticlesSection)
class ArticlesSectionAdmin(TranslationAdmin):
    filter_horizontal = ("articles",)


@admin.register(HeroSection)
class HomeHeroAdmin(TranslationAdmin):
    list_display = ("headline", "cta_link", "image", "allow_translation")
    list_editable = ("cta_link", "image", "allow_translation")
    list_filter = ("home", "allow_translation")
    actions = translation_actions
