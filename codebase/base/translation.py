from modeltranslation.translator import TranslationOptions, register

from .models import MenuItem, PageLink


@register(MenuItem)
class MenuItemOptions(TranslationOptions):
    fields = ("title",)


@register(PageLink)
class PageLinkOptions(TranslationOptions):
    fields = ("external_title",)
