from modeltranslation.translator import TranslationOptions, register

from .models import Link


@register(Link)
class LinkOptions(TranslationOptions):
    fields = ("custom_title",)
