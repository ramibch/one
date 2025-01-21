from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

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

    def get_default_language(self) -> str:
        return settings.LANGUAGE_CODE

    def get_rest_languages(self) -> set:
        return {lang for site in self.sites.all() for lang in site.rest_languages}

    def __str__(self):
        joined_sites = ", ".join([site.domain for site in self.sites.all()])
        return f"{self.question} [🌐 {joined_sites}]"
