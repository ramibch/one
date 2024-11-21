from modeltranslation.translator import TranslationOptions, register

from .models import HeroSection, HomePage


@register(HomePage)
class HomePageOptions(TranslationOptions):
    fields = ("title", "benefits_title", "steps_title", "faqs_title")


@register(HeroSection)
class HomePageHeroOptions(TranslationOptions):
    fields = ("headline", "subheadline", "cta_title")
