from modeltranslation.translator import TranslationOptions, register

from .models import FooterItem


@register(FooterItem)
class FooterItemOptions(TranslationOptions):
    fields = ("title",)
