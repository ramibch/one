from auto_prefetch import ForeignKey, OneToOneField
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from one.articles.models import Article

from ..base.utils.abstracts import TranslatableModel
from ..faqs.models import FAQ


class LandingPage(TranslatableModel):
    LANG_ATTR = "site__language"
    LANGS_ATTR = "site__languages"
    I18N_SLUGIFY_FROM = "title"

    site = ForeignKey("sites.Site", on_delete=models.CASCADE)
    title = models.CharField(max_length=128, default="")
    slug = models.SlugField(max_length=128, null=True, blank=True)
    is_home = models.BooleanField(default=True)
    benefits_title = models.CharField(max_length=64, null=True, blank=True)

    def clean(self) -> None:
        home_exits = LandingPage.objects.filter(site=self.site, is_home=True).exists()
        if home_exits and self.is_home is True:
            raise ValidationError(_("Home already exists"), code="unique_home_per_site")
        return super().clean()

    def get_absolute_url(self):
        if self.is_home:
            return reverse_lazy("home")
        return reverse_lazy("slug_page", kwargs={"slug": self.slug})

    @cached_property
    def url(self):
        return self.get_absolute_url()

    def __str__(self):
        return f"{self.title}"


class _ChildModel(TranslatableModel):
    LANG_ATTR = "landing__site__language"
    LANGS_ATTR = "landing__site__languages"
    landing = OneToOneField(LandingPage, on_delete=models.CASCADE)

    class Meta(TranslatableModel.Meta):
        abstract = True


class ArticlesSection(_ChildModel):
    emoji = models.CharField(max_length=8, db_default="📝")
    title = models.CharField(max_length=64)
    number_of_articles = models.PositiveSmallIntegerField(default=6)
    show_all_link = models.BooleanField(db_default=True)
    show_created_on = models.BooleanField(db_default=True)
    card_animation = ForeignKey(
        "base.Animation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    class Meta(_ChildModel.Meta):
        verbose_name = _("Articles Section")
        verbose_name_plural = _("Articles Sections")

    def __str__(self):
        return self.title

    @cached_property
    def articles(self):
        return (
            Article.objects.filter(
                main_topic__name__in=self.landing.site.topics,
                languages__contains=[get_language()],
                slug__isnull=False,
            )
            .order_by("-id")
            .distinct()
        )[: self.number_of_articles]

    @cached_property
    def articles_available(self):
        return self.articles.count() > 0


class HeroSection(_ChildModel):
    headline = models.TextField(max_length=256)
    subheadline = models.TextField(max_length=256)
    image = models.ImageField(upload_to="homepages/hero/")
    cta_link = ForeignKey("links.Link", on_delete=models.CASCADE, related_name="+")
    cta_title = models.CharField(max_length=64, null=True, blank=True)
    cta_new_tab = models.BooleanField(default=False)
    cta_animation = ForeignKey(
        "base.Animation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    def __str__(self):
        return f"{self.headline} - {self.landing}"

    @cached_property
    def display_cta_title(self):
        return self.cta_title if self.cta_title else self.cta_link.title


class ProblemSection(_ChildModel):
    title = models.CharField(max_length=128)
    description = models.TextField(
        help_text=_("Reflect here the problem of the user. Use bullet list")
    )
    emoji = models.CharField(max_length=8, db_default="⚠️")

    def __str__(self):
        return self.title


class SolutionSection(_ChildModel):
    title = models.CharField(max_length=128)
    description = models.TextField(
        help_text=_("Introduce our product/service as the solution.")
    )
    emoji = models.CharField(max_length=8, db_default="💡")

    def __str__(self):
        return self.title


class BenefitItem(TranslatableModel):
    landing = ForeignKey(LandingPage, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=8, db_default="🚀")
    name = models.CharField(max_length=32)
    description = models.TextField()


class StepActionSection(_ChildModel):
    title = models.CharField(max_length=128)
    description = models.TextField()


class FAQsSection(_ChildModel):
    title = models.CharField(max_length=128)
    categories = models.ManyToManyField("faqs.FAQCategory")

    class Meta(_ChildModel.Meta):
        verbose_name = _("FAQs Section")
        verbose_name_plural = _("FAQs Sections")

    def __str__(self):
        return self.title

    @cached_property
    def faqs(self):
        return (
            FAQ.objects.filter(
                categories__in=self.categories.all(),
                sites=self.landing.site,
            )
            .order_by("-id")
            .distinct()
        )


class FinalCTASection(_ChildModel):
    title = models.TextField(max_length=256)
    description = models.TextField()
    cta_link = ForeignKey("links.Link", on_delete=models.CASCADE, related_name="+")
    cta_title = models.CharField(max_length=64, null=True, blank=True)
    cta_new_tab = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.landing}"

    @cached_property
    def display_cta_title(self):
        return self.cta_title if self.cta_title else self.cta_link.title
