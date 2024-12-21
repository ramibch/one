from auto_prefetch import ForeignKey, Model, OneToOneField
from django.db import models
from django.utils.translation import gettext_lazy as _

from codebase.base.utils.mixins import PageMixin

from ..base.utils.abstracts import TranslatableModel
from ..base.utils.db_fields import ChoiceArrayField
from ..faqs.models import FAQCategory


class Home(TranslatableModel, PageMixin):
    site = OneToOneField("sites.Site", on_delete=models.CASCADE)
    title = models.CharField(max_length=64, default="")

    # Management
    enable_section_changing = models.BooleanField(default=False)
    display_last_articles = models.BooleanField(default=False)
    num_articles = models.PositiveSmallIntegerField(default=6)
    display_faqs = models.BooleanField(default=False)

    # Titles
    benefits_title = models.CharField(max_length=64, null=True, blank=True)
    steps_title = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f"{self.title} 🌐{self.site}"

    # Translation

    def get_default_language(self):
        return self.site.default_language

    def get_rest_languages(self):
        return self.site.rest_languages


class HeroSection(TranslatableModel):
    home = OneToOneField("home.Home", on_delete=models.CASCADE)
    headline = models.TextField(max_length=256)
    subheadline = models.TextField(max_length=256)
    cta_link = ForeignKey("links.Link", on_delete=models.CASCADE)
    cta_title = models.CharField(max_length=64, null=True, blank=True)
    cta_new_tab = models.BooleanField(default=False)
    image = models.ImageField(upload_to="homepages/hero/")

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

    home = OneToOneField("home.Home", on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()

    def get_default_language(self):
        return self.home.site.default_language

    def get_rest_languages(self):
        return self.home.site.rest_languages


class SolutionSection(TranslatableModel):
    home = OneToOneField("home.Home", on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()

    def get_default_language(self):
        return self.home.site.default_language

    def get_rest_languages(self):
        return self.home.site.rest_languages


class BenefitsSection(TranslatableModel):
    home = OneToOneField("home.Home", on_delete=models.CASCADE)
    emoji = models.CharField(max_length=8)

    def get_default_language(self):
        return self.home.site.default_language

    def get_rest_languages(self):
        return self.home.site.rest_languages


class StepAction(TranslatableModel):
    home = ForeignKey("home.Home", on_delete=models.CASCADE)
    step_label = models.CharField(max_length=4, default="01")
    title = models.CharField(max_length=64)
    description = models.TextField()

    def get_default_language(self):
        return self.home.site.default_language

    def get_rest_languages(self):
        return self.home.site.rest_languages


class FAQsSection(TranslatableModel):
    home = OneToOneField("home.Home", on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    faqs = models.ManyToManyField("faqs.FAQ", limit_choices_to={"featured": True})
    auto_add_categories = ChoiceArrayField(
        models.CharField(max_length=32, choices=FAQCategory)
    )
    auto_add_faqs = models.BooleanField(default=False)

    def get_default_language(self):
        return self.home.site.default_language

    def get_rest_languages(self):
        return self.home.site.rest_languages

    class Meta(TranslatableModel.Meta):
        verbose_name = _("FAQs Section")
        verbose_name_plural = _("FAQs Sections")

    def __str__(self):
        return self.title


class ArticlesSection(TranslatableModel):
    home = OneToOneField("home.Home", on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    articles = models.ManyToManyField("articles.Article")
    auto_add_articles = models.BooleanField(default=False)

    def get_default_language(self):
        return self.home.site.default_language

    def get_rest_languages(self):
        return self.home.site.rest_languages

    class Meta(TranslatableModel.Meta):
        verbose_name = _("Articles Section")
        verbose_name_plural = _("Articles Sections")

    def __str__(self):
        return self.title


class UserHome(TranslatableModel, PageMixin):
    site = OneToOneField("sites.Site", on_delete=models.CASCADE)

    def get_default_language(self):
        return self.site.default_language

    def get_rest_languages(self):
        return self.site.rest_languages
