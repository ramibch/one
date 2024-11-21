from auto_prefetch import Model
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy as _


class FAQCategories(models.TextChoices):
    PLANS = "plans", _("Plans")
    PRODUCTS = "products", _("Products")
    INFO = "info", _("Informative")
    ACCOUNTS = "accounts", _("Accounts")
    LEGAL = "legal", _("Legal concerns")


class FAQ(Model):
    sites = models.ManyToManyField(Site)
    category = models.CharField(max_length=32, choices=FAQCategories)
    question = models.CharField(max_length=256)
    answer = models.TextField()

    can_be_shown_in_home = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.answer
