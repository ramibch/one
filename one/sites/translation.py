from modeltranslation.translator import TranslationOptions, register

from .models import Seo


@register(Seo)
class SeoOptions(TranslationOptions):
    fields = ("page_title", "page_description", "page_keywords")
