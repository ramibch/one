from modeltranslation.translator import TranslationOptions, register

from .models import Product


@register(Product)
class ProductOptions(TranslationOptions):
    fields = ("title", "summary")
