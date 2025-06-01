from django.contrib import admin
from django.db import IntegrityError
from modeltranslation.admin import TranslationStackedInline

from one.admin import (
    OneTranslatableModelAdmin,
    OneTranslationStackedInline,
)

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


class ProblemSectionInline(OneTranslationStackedInline):
    model = ProblemSection
    extra = 0


class SolutionSectionInline(OneTranslationStackedInline):
    model = SolutionSection
    extra = 0


class BenefitItemInline(TranslationStackedInline):
    model = BenefitItem
    extra = 0


class StepActionSectionInline(TranslationStackedInline):
    model = StepActionSection
    extra = 0


class ArticlesSectionInline(OneTranslationStackedInline):
    model = ArticlesSection
    extra = 0


class FAQsSectionInline(OneTranslationStackedInline):
    model = FAQsSection
    extra = 0


class FinalCTASectionInline(TranslationStackedInline):
    model = FinalCTASection
    extra = 0


@admin.register(LandingPage)
class LandingPageAdmin(OneTranslatableModelAdmin):
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
class HeroSectionAdmin(OneTranslatableModelAdmin):
    list_display = ("landing", "landing__site", "headline", "cta_link")
    list_filter = ("landing__site",)


@admin.register(ProblemSection)
class ProblemSectionAdmin(OneTranslatableModelAdmin):
    list_display = ("landing", "landing__site", "title", "emoji")
    list_filter = ("landing__site",)


@admin.register(SolutionSection)
class SolutionSectionAdmin(OneTranslatableModelAdmin):
    list_display = ("landing", "landing__site", "title", "emoji")
    list_filter = ("landing__site",)


@admin.register(BenefitItem)
class BenefitItemAdmin(OneTranslatableModelAdmin):
    list_display = ("landing", "landing__site", "name_en", "emoji", "description")
    list_filter = ("landing__site",)
    list_editable = ("name_en", "emoji")


@admin.register(ArticlesSection)
class ArticlesSectionAdmin(OneTranslatableModelAdmin):
    pass


@admin.register(StepActionSection)
class StepActionSectionAdmin(OneTranslatableModelAdmin):
    list_display = ("landing", "landing__site")
