from auto_prefetch import ForeignKey, Model, OneToOneField
from django.db import models
from django.db.models import Q
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from one.base.utils.mixins import PageMixin

from ..base.utils.abstracts import TranslatableModel
from ..base.utils.animate import (
    AnimationDelay,
    AnimationRepeat,
    AnimationSpeed,
    AnimationType,
    AttentionSeekers,
)
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


class HeroSection(TranslatableModel):
    home = OneToOneField("home.Home", on_delete=models.CASCADE)
    headline = models.TextField(max_length=256)
    subheadline = models.TextField(max_length=256)
    image = models.ImageField(upload_to="homepages/hero/")
    cta_link = ForeignKey("links.Link", on_delete=models.CASCADE)
    cta_title = models.CharField(max_length=64, null=True, blank=True)
    cta_new_tab = models.BooleanField(default=False)
    cta_animation_type = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        default=AnimationType.VANILLA,
        choices=AnimationType,
    )
    cta_animation_name = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        default=AttentionSeekers.FLASH,
        choices=AttentionSeekers,
    )
    cta_animation_repeat = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        default=AnimationRepeat.ONE,
        choices=AnimationRepeat,
    )
    cta_animation_speed = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=AnimationSpeed,
    )
    cta_animation_delay = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=AnimationDelay,
    )

    def __str__(self):
        return f"{self.headline} - {self.home}"

    def display_cta_title(self):
        return self.cta_title if self.cta_title else self.cta_link.title


class ProblemSection(Model):
    """ """

    home = OneToOneField("home.Home", on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()


class SolutionSection(TranslatableModel):
    home = OneToOneField("home.Home", on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()


class BenefitsSection(TranslatableModel):
    home = OneToOneField("home.Home", on_delete=models.CASCADE)
    emoji = models.CharField(max_length=8)


class StepAction(TranslatableModel):
    home = ForeignKey("home.Home", on_delete=models.CASCADE)
    step_label = models.CharField(max_length=4, default="01")
    title = models.CharField(max_length=64)
    description = models.TextField()


class FAQsSection(TranslatableModel):
    home = OneToOneField("home.Home", on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    faqs = models.ManyToManyField("faqs.FAQ", limit_choices_to={"featured": True})
    auto_add_categories = ChoiceArrayField(
        models.CharField(max_length=32, choices=FAQCategory)
    )
    auto_add_faqs = models.BooleanField(default=False)

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
    number_of_articles = models.PositiveSmallIntegerField(default=6)
    card_animation_type = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        default=AnimationType.ON_MOUSE_OVER,
        choices=AnimationType,
    )
    card_animation_name = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        default=AttentionSeekers.PULSE,
        choices=AttentionSeekers,
    )

    card_animation_repeat = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        default=AnimationRepeat.ONE,
        choices=AnimationRepeat,
    )
    card_animation_speed = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=AnimationSpeed,
    )
    card_animation_delay = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=AnimationDelay,
    )

    def get_articles(self):
        lang = get_language()
        return (
            self.articles.filter(
                Q(default_language=lang) | Q(rest_languages__contains=[lang])
            )
            .exclude(slug=None, featured=False)
            .distinct()[: self.number_of_articles]
        )

    class Meta(TranslatableModel.Meta):
        verbose_name = _("Articles Section")
        verbose_name_plural = _("Articles Sections")

    def __str__(self):
        return self.title
