from modeltranslation.translator import TranslationOptions, register

from .models import Page


@register(Page)
class PageOptions(TranslationOptions):
    fields = ("title", "body", "slug")
