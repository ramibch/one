from modeltranslation.translator import TranslationOptions, register

from .models import (
    ArticlesSection,
    BenefitItem,
    FAQsSection,
    FinalCTASection,
    HeroSection,
    LandingPage,
    ProblemSection,
    SolutionSection,
    StepActionSection,
)


@register(LandingPage)
class LandingPageOptions(TranslationOptions):
    fields = ("title", "slug")


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


@register(BenefitItem)
class BenefitItemOptions(TranslationOptions):
    fields = ("name", "description")


@register(StepActionSection)
class StepActionSectionOptions(TranslationOptions):
    fields = ("title", "description")


@register(FinalCTASection)
class FinalCTASectionOptions(TranslationOptions):
    fields = ("title", "description", "cta_title")
