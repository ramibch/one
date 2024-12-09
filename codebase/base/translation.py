from modeltranslation.translator import TranslationOptions, register

from .models import Topic


@register(Topic)
class FAQOptions(TranslationOptions):
    fields = ("name", "slug")
