from django.contrib import admin
from modeltranslation.admin import TranslationStackedInline

from one.base.utils.admin import FORMFIELD_OVERRIDES_DICT, TranslatableModelAdmin

from .models import (
    ArticlesSection,
    BenefitItem,
    FAQsSection,
    HeroSection,
    Home,
    ProblemSection,
    SolutionSection,
    StepAction,
)


class HeroSectionInline(TranslationStackedInline):
    model = HeroSection
    extra = 0


class ProblemSectionInline(TranslationStackedInline):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    model = ProblemSection
    extra = 0


class SolutionSectionInline(TranslationStackedInline):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    model = SolutionSection
    extra = 0


class BenefitItemInline(TranslationStackedInline):
    model = BenefitItem
    extra = 0


class StepActionInline(TranslationStackedInline):
    model = StepAction
    extra = 0


class ArticlesSectionInline(TranslationStackedInline):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    model = ArticlesSection
    extra = 0


class FAQsSectionInline(TranslationStackedInline):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    model = FAQsSection
    extra = 0


@admin.register(Home)
class HomeAdmin(TranslatableModelAdmin):
    list_display = ("__str__", "title", "site")
    inlines = (
        HeroSectionInline,
        ProblemSectionInline,
        SolutionSectionInline,
        BenefitItemInline,
        StepActionInline,
        ArticlesSectionInline,
        FAQsSectionInline,
    )
