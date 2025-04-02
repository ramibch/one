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
    LANG_ATTR = "sites__language"
    LANGS_ATTR = "sites__languages"
    sites = models.ManyToManyField("sites.Site")
    category = models.CharField(max_length=32, choices=FAQCategory)
    question = models.CharField(max_length=256)
    answer = models.TextField()
    featured = models.BooleanField(default=False)

    def __str__(self):
        joined_sites = ", ".join([site.domain for site in self.sites.all()])
        return f"{self.question} [🌐 {joined_sites}]"
