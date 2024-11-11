from modeltranslation.translator import TranslationOptions, register

from .models import FooterItem, SocialMediaLink


@register(FooterItem)
class FooterItemOptions(TranslationOptions):
    fields = ("title",)


@register(SocialMediaLink)
class SocialMediaLinkOptions(TranslationOptions):
    fields = ("url",)
