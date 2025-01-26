from modeltranslation.translator import TranslationOptions, register

from .models import Site


@register(Site)
class SiteOptions(TranslationOptions):
    fields = ("page_title", "page_description", "page_keywords")
