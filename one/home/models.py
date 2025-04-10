from auto_prefetch import ForeignKey, OneToOneField
from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from one.articles.models import Article

from ..base.utils.abstracts import TranslatableModel
from ..base.utils.db import ChoiceArrayField
from ..faqs.models import FAQ, FAQCategory


class Home(TranslatableModel):
    LANG_ATTR = "site__language"
    LANGS_ATTR = "site__languages"

    site = OneToOneField("sites.Site", on_delete=models.CASCADE)
    title = models.CharField(max_length=64, default="")
    benefits_title = models.CharField(max_length=64, null=True, blank=True)
    steps_title = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f"{self.title} 🌐{self.site}"


class HomeChildModel(TranslatableModel):
    LANG_ATTR = "home__site__language"
    LANGS_ATTR = "home__site__languages"
    home = OneToOneField(Home, on_delete=models.CASCADE)

    class Meta(TranslatableModel.Meta):
        abstract = True


class ArticlesSection(HomeChildModel):
    title = models.CharField(max_length=64)
    number_of_articles = models.PositiveSmallIntegerField(default=6)
    card_animation = ForeignKey(
        "base.Animation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta(HomeChildModel.Meta):
        verbose_name = _("Articles Section")
        verbose_name_plural = _("Articles Sections")

    def __str__(self):
        return self.title

    def get_articles(self):
        return (
            Article.objects.filter(
                parent_folder__topics__in=self.home.site.topics.all(),
                languages__contains=[get_language()],
                slug__isnull=False,
            )
            .order_by("-id")
            .distinct()
        )[: self.number_of_articles]


class HeroSection(HomeChildModel):
    headline = models.TextField(max_length=256)
    subheadline = models.TextField(max_length=256)
    image = models.ImageField(upload_to="homepages/hero/")
    cta_link = ForeignKey("links.Link", on_delete=models.CASCADE)
    cta_title = models.CharField(max_length=64, null=True, blank=True)
    cta_new_tab = models.BooleanField(default=False)
    cta_animation = ForeignKey(
        "base.Animation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.headline} - {self.home}"

    def display_cta_title(self):
        return self.cta_title if self.cta_title else self.cta_link.title


class ProblemSection(HomeChildModel):
    title = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.title


class SolutionSection(HomeChildModel):
    title = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.title


class BenefitItem(TranslatableModel):
    home = ForeignKey(Home, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    description = models.TextField()


class StepAction(HomeChildModel):
    home = ForeignKey(Home, on_delete=models.CASCADE)
    step_label = models.CharField(max_length=4, default="01")
    title = models.CharField(max_length=64)
    description = models.TextField()


class FAQsSection(HomeChildModel):
    title = models.CharField(max_length=64)
    categories = ChoiceArrayField(models.CharField(max_length=32, choices=FAQCategory))

    class Meta(HomeChildModel.Meta):
        verbose_name = _("FAQs Section")
        verbose_name_plural = _("FAQs Sections")

    def __str__(self):
        return self.title

    def get_faqs(self):
        return (
            FAQ.objects.filter(
                category__in=self.categories,
                languages__contains=[get_language()],
                sites=self.home.site,
                featured=True,
            )
            .order_by("-id")
            .distinct()
        )
