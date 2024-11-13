from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from modeltranslation.admin import TranslationAdmin

from ..utils.actions import translation_actions
from .models import FooterItem, FooterLink, NavbarLink, SocialMediaLink

FORMFIELD_OVERRIDES_DICT = {
    models.ManyToManyField: {"widget": CheckboxSelectMultiple},
}


@admin.register(NavbarLink)
class NavbarLinkAdmin(admin.ModelAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("display_title", "emoji", "show_type", "show_as_emoji", "new_tab", "order")
    list_filter = ("show_type", "show_as_emoji", "new_tab", "order")
    list_editable = ("show_type", "order", "emoji", "show_as_emoji", "new_tab")


class FooterLinkInline(admin.StackedInline):
    model = FooterLink
    extra = 1
    exclude = ("site",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(footer_item__isnull=False)


@admin.register(FooterItem)
class FooterItemAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("display_title", "emoji", "show_type", "order")
    list_editable = ("emoji", "show_type", "order")
    list_filter = ("show_type", "order")
    inlines = (FooterLinkInline,)
    actions = translation_actions


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("display_title", "footer_item", "show_type", "new_tab", "order")
    list_editable = ("show_type", "footer_item", "new_tab", "order")
    list_filter = ("show_type", "order", "new_tab", "footer_item")


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("platform", "new_tab", "show_type", "order")
    list_editable = ("show_type", "new_tab", "order")
    list_filter = ("show_type", "new_tab", "order")
