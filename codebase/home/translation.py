from modeltranslation.translator import TranslationOptions, register

from .models import Hero, HeroCTA, HomePage


@register(HomePage)
class HomePageOptions(TranslationOptions):
    fields = ("title",)


@register(Hero)
class HeroOptions(TranslationOptions):
    fields = ("headline", "subheadline")


@register(HeroCTA)
class HeroCTAOptions(TranslationOptions):
    fields = ("custom_title",)
