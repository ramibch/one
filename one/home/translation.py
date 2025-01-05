from modeltranslation.translator import TranslationOptions, register

from .models import ArticlesSection, FAQsSection, HeroSection, Home


@register(Home)
class HomeOptions(TranslationOptions):
    fields = ("title",)


@register(HeroSection)
class HeroSectionOptions(TranslationOptions):
    fields = ("headline", "subheadline", "cta_title")


@register(ArticlesSection)
class ArticlesSectionOptions(TranslationOptions):
    fields = ("title",)


@register(FAQsSection)
class FAQsSectionOptions(TranslationOptions):
    fields = ("title",)
