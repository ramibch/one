from modeltranslation.translator import TranslationOptions, register

from .models import Shop


@register(Shop)
class ShopOptions(TranslationOptions):
    fields = ("general_listing_description",)
