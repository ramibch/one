from auto_prefetch import ForeignKey, Model
from django.contrib.sites.models import Site
from django.db import models
from django.utils.functional import cached_property

from ..faqs.models import FAQ
from ..links.models import Link
from ..utils.mixins import PageMixin


class HomePage(Model, PageMixin):
    sites = models.ManyToManyField(Site)

    # Management
    is_active = models.BooleanField(default=True)
    display_last_articles = models.BooleanField(default=False)
    display_faqs = models.BooleanField(default=False)
    enable_section_changing = models.BooleanField(default=False)
    allow_translation = models.BooleanField(default=False)

    # Titles
    title = models.CharField(max_length=64)
    benefits_title = models.CharField(max_length=64, null=True, blank=True)
    steps_title = models.CharField(max_length=64, null=True, blank=True)
    faqs_title = models.CharField(max_length=64, null=True, blank=True)

    @cached_property
    def hero_section(self):
        return self.herosection_set.filter(is_active=True).first()

    @cached_property
    def problem_section(self):
        return self.problemsection_set.filter(is_active=True).first()

    @cached_property
    def faqs(self):
        return FAQ.objects.filter(
            sites=self.sites, can_be_shown_in_home=True, is_active=True
        ).distinct()


class HeroSection(Model):
    homepage = ForeignKey(HomePage, on_delete=models.CASCADE)
    headline = models.TextField(max_length=256)
    subheadline = models.TextField(max_length=256)
    cta_link = ForeignKey(Link, on_delete=models.CASCADE)
    cta_title = models.CharField(max_length=64, null=True, blank=True)
    cta_new_tab = models.BooleanField(default=False)
    image = models.ImageField(upload_to="homepages/hero/")
    is_active = models.BooleanField()
    allow_translation = models.BooleanField(default=False)

    def display_cta_title(self):
        return self.cta_title if self.cta_title else self.cta_link.title

    def __str__(self):
        return f"{self.headline} - {self.homepage}"


class ProblemSection(Model):
    """ """

    homepage = ForeignKey(HomePage, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    is_active = models.BooleanField()


class SolutionSection(Model):
    homepage = ForeignKey(HomePage, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    is_active = models.BooleanField()


class BenefitsSection(Model):
    homepage = ForeignKey(HomePage, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=8)
    is_active = models.BooleanField()


class StepAction(Model):
    homepage = ForeignKey(HomePage, on_delete=models.CASCADE)
    step_label = models.CharField(max_length=4, default="01")
    title = models.CharField(max_length=64)
    description = models.TextField()
    is_active = models.BooleanField()


class UserHomePage(Model, PageMixin):
    sites = models.ManyToManyField(Site)
    allow_translation = models.BooleanField(default=False)
