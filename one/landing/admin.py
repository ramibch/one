from django.contrib import admin
from django.db import IntegrityError
from modeltranslation.admin import TranslationStackedInline

from one.admin import FORMFIELD_OVERRIDES_DICT, TranslatableModelAdmin

from .factories import (
    ArticlesSectionFactory,
    BenefitItemFactory,
    FAQsSectionFactory,
    FinalCTASectionFactory,
    HeroSectionFactory,
    ProblemSectionFactory,
    SolutionSectionFactory,
    StepActionSectionFactory,
)
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


class StepActionSectionInline(TranslationStackedInline):
    model = StepActionSection
    extra = 0


class ArticlesSectionInline(TranslationStackedInline):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    model = ArticlesSection
    extra = 0


class FAQsSectionInline(TranslationStackedInline):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    model = FAQsSection
    extra = 0


class FinalCTASectionInline(TranslationStackedInline):
    model = FinalCTASection
    extra = 0


@admin.register(LandingPage)
class LandingPageAdmin(TranslatableModelAdmin):
    list_display = ("__str__", "title", "site")
    inlines = (
        HeroSectionInline,
        ProblemSectionInline,
        SolutionSectionInline,
        BenefitItemInline,
        StepActionSectionInline,
        ArticlesSectionInline,
        FAQsSectionInline,
        FinalCTASectionInline,
    )
    actions = ["fake_sections"]

    @admin.action(description="🏭 Fake sections")
    def fake_sections(modeladmin, request, queryset):
        OneTwoOneModels = [
            HeroSectionFactory,
            ArticlesSectionFactory,
            HeroSectionFactory,
            ProblemSectionFactory,
            SolutionSectionFactory,
            FAQsSectionFactory,
            StepActionSectionFactory,
            FinalCTASectionFactory,
        ]

        for home in queryset:
            if not home.benefititem_set.filter().exists():
                BenefitItemFactory.create_batch(6, home=home)

            for OneTwoOneModel in OneTwoOneModels:
                try:
                    OneTwoOneModel(home=home)
                except IntegrityError:
                    pass


@admin.register(HeroSection)
class HeroSectionAdmin(TranslatableModelAdmin):
    list_display = ("landing", "landing__site", "headline", "cta_link")
    list_filter = ("landing__site",)


@admin.register(ProblemSection)
class ProblemSectionAdmin(TranslatableModelAdmin):
    list_display = ("landing", "landing__site", "title", "emoji")
    list_filter = ("landing__site",)


@admin.register(SolutionSection)
class SolutionSectionAdmin(TranslatableModelAdmin):
    list_display = ("landing", "landing__site", "title", "emoji")
    list_filter = ("landing__site",)


@admin.register(BenefitItem)
class BenefitItemAdmin(TranslatableModelAdmin):
    list_display = ("landing", "landing__site", "name_en", "emoji", "description")
    list_filter = ("landing__site",)
    list_editable = ("name_en", "emoji")


@admin.register(ArticlesSection)
class ArticlesSectionAdmin(TranslatableModelAdmin):
    pass


@admin.register(StepActionSection)
class StepActionSectionAdmin(TranslatableModelAdmin):
    list_display = ("landing", "landing__site")
