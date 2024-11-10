from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

from ..utils.actions import translate_from_default_language
from .models import FooterItem, FooterLink, NavbarLink, SocialMediaLink

FORMFIELD_OVERRIDES_DICT = {
    models.ManyToManyField: {"widget": CheckboxSelectMultiple},
}


@admin.register(NavbarLink)
class NavbarLinkAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("display_title", "emoji", "show_type", "show_as_emoji", "new_tab", "order")
    list_filter = ("show_type", "show_as_emoji", "new_tab", "order")
    list_editable = ("show_type", "order", "emoji", "show_as_emoji", "new_tab")
    actions = [translate_from_default_language]


class FooterLinkInline(TranslationStackedInline):
    model = FooterLink
    extra = 1
    exclude = ("site",)


@admin.register(FooterItem)
class FooterItemAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("display_title", "title", "show_type", "order")
    list_editable = ("show_type", "order")
    list_filter = ("show_type", "order")
    inlines = (FooterLinkInline,)
    actions = [translate_from_default_language]


@admin.register(FooterLink)
class FooterLinkAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("display_title", "footer_item", "show_type", "new_tab", "order")
    list_editable = ("show_type", "footer_item", "new_tab", "order")
    list_filter = ("show_type", "order", "new_tab", "footer_item")
    actions = [translate_from_default_language]


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("platform", "new_tab", "show_type", "order")
    list_editable = ("show_type", "new_tab", "order")
    list_filter = ("show_type", "new_tab", "order")
    actions = [translate_from_default_language]
