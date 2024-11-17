from auto_prefetch import Model
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy as _


class FAQ(Model):
    FAQ_CATEGORY_CHOICES = (
        ("plans", _("Plans")),
        ("products", _("Products")),
        ("info", _("Informative")),
        ("accounts", _("Accounts")),
        ("legal", _("Legal concerns")),
    )
    sites = models.ManyToManyField(Site)
    category = models.CharField(max_length=32, choices=FAQ_CATEGORY_CHOICES)
    question = models.CharField(max_length=256)
    answer = models.TextField()