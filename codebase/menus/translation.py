from modeltranslation.translator import TranslationOptions, register

from .models import MenuItem, PageLink, SocialMediaLink


@register(MenuItem)
class MenuItemOptions(TranslationOptions):
    fields = ("title",)


@register(PageLink)
class PageLinkOptions(TranslationOptions):
    fields = ("custom_title",)

@register(SocialMediaLink)
class SocialMediaLinkOptions(TranslationOptions):
    fields = ("title", "url")
