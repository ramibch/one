from modeltranslation.translator import TranslationOptions, register

from .models import FAQ



@register(FAQ)
class FAQOptions(TranslationOptions):
    fields = ("question", "answer")
