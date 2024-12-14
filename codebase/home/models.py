from auto_prefetch import ForeignKey, Model, OneToOneField
from django.db import models
from django.utils.functional import cached_property

from codebase.base.utils.mixins import PageMixin

from ..articles.models import Article, ArticlesSubmodule
from ..base.utils.abstracts import TranslatableModel
from ..faqs.models import FAQ


class Home(TranslatableModel, PageMixin):
    site = OneToOneField("sites.Site", on_delete=models.CASCADE)

    # Management
    is_active = models.BooleanField(default=True)
    enable_section_changing = models.BooleanField(default=False)
    display_last_articles = models.BooleanField(default=False)
    num_articles = models.PositiveSmallIntegerField(default=6)
    display_faqs = models.BooleanField(default=False)

    # Titles
    title = models.CharField(max_length=64)
    benefits_title = models.CharField(max_length=64, null=True, blank=True)
    steps_title = models.CharField(max_length=64, null=True, blank=True)
    faqs_title = models.CharField(max_length=64, null=True, blank=True)

    # Sections

    @cached_property
    def hero_section(self):
        return self.herosection_set.filter(is_active=True).first()

    @cached_property
    def problem_section(self):
        return self.problemsection_set.filter(is_active=True).first()

    @cached_property
    def last_articles(self):
        sites = self.sites.values_list("site", flat=True)
        folders = ArticlesSubmodule.objects.filter(site__in=sites).distinct()
        return Article.objects.filter(submodule_folder__in=folders)[: self.num_articles]

    @cached_property
    def faqs(self):
        return FAQ.objects.filter(
            sites=self.sites, can_be_shown_in_home=True, is_active=True
        ).distinct()

    # tranlation

    def get_default_language(self):
        return self.site.default_language

    def get_rest_languages(self):
        return self.site.rest_languages


class HomeHeroSection(TranslatableModel):
    home = ForeignKey("home.Home", on_delete=models.CASCADE)
    headline = models.TextField(max_length=256)
    subheadline = models.TextField(max_length=256)
    cta_link = ForeignKey("links.Link", on_delete=models.CASCADE)
    cta_title = models.CharField(max_length=64, null=True, blank=True)
    cta_new_tab = models.BooleanField(default=False)
    image = models.ImageField(upload_to="homepages/hero/")
    is_active = models.BooleanField()

    def __str__(self):
        return f"{self.headline} - {self.home}"

    def display_cta_title(self):
        return self.cta_title if self.cta_title else self.cta_link.title

    def get_default_language(self):
        return self.home.site.default_language

    def get_rest_languages(self):
        return self.home.site.rest_languages


class ProblemSection(Model):
    """ """

    home = ForeignKey("home.Home", on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    is_active = models.BooleanField()

    def get_default_language(self):
        return self.home.site.default_language

    def get_rest_languages(self):
        return self.home.site.rest_languages


class SolutionSection(TranslatableModel):
    home = ForeignKey("home.Home", on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    is_active = models.BooleanField()

    def get_default_language(self):
        return self.home.site.default_language

    def get_rest_languages(self):
        return self.home.site.rest_languages


class BenefitsSection(TranslatableModel):
    home = ForeignKey("home.Home", on_delete=models.CASCADE)
    emoji = models.CharField(max_length=8)
    is_active = models.BooleanField()

    def get_default_language(self):
        return self.home.site.default_language

    def get_rest_languages(self):
        return self.home.site.rest_languages


class StepAction(TranslatableModel):
    home = ForeignKey("home.Home", on_delete=models.CASCADE)
    step_label = models.CharField(max_length=4, default="01")
    title = models.CharField(max_length=64)
    description = models.TextField()
    is_active = models.BooleanField()

    def get_default_language(self):
        return self.home.site.default_language

    def get_rest_languages(self):
        return self.home.site.rest_languages


class UserHome(TranslatableModel, PageMixin):
    site = OneToOneField("sites.Site", on_delete=models.CASCADE)

    def get_default_language(self):
        return self.site.default_language

    def get_rest_languages(self):
        return self.site.rest_languages
