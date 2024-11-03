from modeltranslation.translator import TranslationOptions, register

from .models import FooterItem, FooterLink, NavbarLink, SocialMediaLink


@register(FooterItem)
class FooterItemOptions(TranslationOptions):
    fields = ("title",)


@register(NavbarLink)
class NavbarLinkOptions(TranslationOptions):
    fields = ("custom_title",)


@register(FooterLink)
class FooterLinkOptions(TranslationOptions):
    fields = ("custom_title",)


@register(SocialMediaLink)
class SocialMediaLinkOptions(TranslationOptions):
    fields = ("url",)
