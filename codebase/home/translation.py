from modeltranslation.translator import TranslationOptions, register

from .models import Hero, HomePage


@register(HomePage)
class HomePageOptions(TranslationOptions):
    fields = ("title",)


@register(Hero)
class HeroOptions(TranslationOptions):
    fields = ("headline", "subheadline", "cta_title")
