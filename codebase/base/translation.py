from modeltranslation.translator import TranslationOptions, register

from .models import ExtendedSite


@register(ExtendedSite)
class ExtendedSiteOptions(TranslationOptions):
    fields = (
        "default_page_title",
        "default_page_description",
        "default_page_keywords",
    )
