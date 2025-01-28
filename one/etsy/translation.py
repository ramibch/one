from modeltranslation.translator import TranslationOptions, register

from .models import Shop


@register(Shop)
class ShopOptions(TranslationOptions):
    fields = ("generic_listing_description",)
