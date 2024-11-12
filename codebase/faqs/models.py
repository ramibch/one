from django.db import models
from auto_prefetch import ForeignKey, Model
from django.utils.translation import gettext_lazy as _

from markdownx.models import MarkdownxField




class FAQ(Model):
    FAQ_CATEGORY_CHOICES = (
        ("plans", _("Plans")),
        ("products", _("Products")),
        ("info", _("Informative")),
        ("accounts", _("Accounts")),
        ("legal", _("Legal concerns")),
    )
    category = models.CharField(max_length=32, choices=FAQ_CATEGORY_CHOICES)
    question = models.CharField(max_length=256)
    answer = MarkdownxField()

