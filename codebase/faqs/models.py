from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..base.models import Language
from ..base.utils.abstracts import TranslatableModel


class FAQCategories(models.TextChoices):
    PLANS = "plans", _("Plans")
    PRODUCTS = "products", _("Products")
    INFO = "info", _("Informative")
    ACCOUNTS = "accounts", _("Accounts")
    LEGAL = "legal", _("Legal concerns")


class FAQ(TranslatableModel):
    sites = models.ManyToManyField("sites.Site")
    category = models.CharField(max_length=32, choices=FAQCategories)
    question = models.CharField(max_length=256)
    answer = models.TextField()

    can_be_shown_in_home = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def get_default_language(self):
        return Language.objects.get_or_create(id=settings.LANGUAGE_CODE)[0]

    def get_rest_languages(self):
        return Language.objects.filter(sites_with_rest_languages__in=self.sites.all())

    def __str__(self):
        return self.answer
