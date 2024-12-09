from modeltranslation.translator import TranslationOptions, register

from .models import ListingTag, MenuListItem, Page, Topic


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ("body", "title", "slug", "description")


@register(MenuListItem)
class MenuListItemOptions(TranslationOptions):
    fields = ("title",)


@register(Topic)
class TopicOptions(TranslationOptions):
    fields = ("name", "slug")


@register(ListingTag)
class ListingTagOptions(TranslationOptions):
    fields = ("name",)
