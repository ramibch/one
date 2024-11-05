from django.db import models
from django.utils.translation import gettext_lazy as _

from ..utils.abstracts import AbstractSingletonModel


class Website(AbstractSingletonModel):
    # TODO: Add more fields! Check settings.WEBSITE
    brand_name = models.CharField(max_length=64)
    title = models.TextField()
    last_huey_flush = models.DateTimeField(null=True)

    def __str__(self):
        return self.brand_name

    class Meta(AbstractSingletonModel.Meta):
        verbose_name = _("Website")
        verbose_name_plural = _("Website")
