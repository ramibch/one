from modeltranslation.translator import TranslationOptions, register

from .models import FAQ, FAQCategory


@register(FAQ)
class FAQOptions(TranslationOptions):
    fields = ("question", "answer")


@register(FAQCategory)
class FAQCategoryOptions(TranslationOptions):
    fields = ("name",)
