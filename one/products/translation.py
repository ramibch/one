from modeltranslation.translator import TranslationOptions, register

from .models import EtsyShop, Product


@register(Product)
class ProductOptions(TranslationOptions):
    fields = ("title", "description")


@register(EtsyShop)
class ShopOptions(TranslationOptions):
    fields = ("generic_listing_description",)
