from modeltranslation.translator import TranslationOptions, register

from .models import Home, HomeHeroSection


@register(Home)
class HomeOptions(TranslationOptions):
    fields = ("title", "benefits_title", "steps_title", "faqs_title")


@register(HomeHeroSection)
class HomeHeroOptions(TranslationOptions):
    fields = ("headline", "subheadline", "cta_title")
