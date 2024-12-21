from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..base.models import Language
from ..base.utils.abstracts import TranslatableModel


class FAQCategory(models.TextChoices):
    PLANS = "plans", _("Plans")
    PRODUCTS = "products", _("Products")
    INFO = "info", _("Informative")
    ACCOUNTS = "accounts", _("Accounts")
    LEGAL = "legal", _("Legal concerns")


class FAQ(TranslatableModel):
    sites = models.ManyToManyField("sites.Site")
    category = models.CharField(max_length=32, choices=FAQCategory)
    question = models.CharField(max_length=256)
    answer = models.TextField()
    featured = models.BooleanField(default=False)

    def get_default_language(self):
        return Language.objects.get_or_create(id=settings.LANGUAGE_CODE)[0]

    def get_rest_languages(self):
        return Language.objects.filter(sites_with_rest_languages__in=self.sites.all())

    def __str__(self):
        joined_sites = ", ".join([site.name for site in self.sites.all()])
        return f"{self.question} [🌐 {joined_sites}]"
