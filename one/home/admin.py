from django.contrib import admin
from modeltranslation.admin import TranslationStackedInline

from one.base.utils.admin import FORMFIELD_OVERRIDES_DICT, TranslatableModelAdmin

from .models import ArticlesSection, FAQsSection, HeroSection, Home


class ArticlesSectionInline(TranslationStackedInline):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    model = ArticlesSection
    extra = 0


@admin.register(Home)
class HomeAdmin(TranslatableModelAdmin):
    list_display = ("__str__", "title", "site")
    inlines = (ArticlesSectionInline,)


@admin.register(FAQsSection)
class FAQsSectionAdmin(TranslatableModelAdmin):
    pass


@admin.register(ArticlesSection)
class ArticlesSectionAdmin(TranslatableModelAdmin):
    pass


@admin.register(HeroSection)
class HomeHeroAdmin(TranslatableModelAdmin):
    list_display = ("headline", "cta_link", "image")
    list_editable = ("cta_link", "image")
    list_filter = ("home",)
