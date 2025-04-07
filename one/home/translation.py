from modeltranslation.translator import TranslationOptions, register

from .models import (
    ArticlesSection,
    BenefitItem,
    BenefitsSection,
    FAQsSection,
    HeroSection,
    Home,
    ProblemSection,
    SolutionSection,
)


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


@register(ProblemSection)
class ProblemSectionOptions(TranslationOptions):
    fields = ("title", "description")


@register(SolutionSection)
class SolutionSectionOptions(TranslationOptions):
    fields = ("title", "description")


@register(BenefitsSection)
class BenefitsSectionOptions(TranslationOptions):
    fields = ("title",)


@register(BenefitItem)
class BenefitItemOptions(TranslationOptions):
    fields = ("name", "description")
