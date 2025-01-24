from modeltranslation.translator import TranslationOptions, register

from .models import Listing, Shop


@register(Shop)
class ShopOptions(TranslationOptions):
    fields = ("general_listing_description",)


@register(Listing)
class ListingOptions(TranslationOptions):
    fields = ("title", "summary")
