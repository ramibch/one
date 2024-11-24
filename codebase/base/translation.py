from modeltranslation.translator import TranslationOptions, register

from .models import ExtendedSite


@register(ExtendedSite)
class ExtendedSiteOptions(TranslationOptions):
    fields = ("page_title", "page_description", "page_keywords")
