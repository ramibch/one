from django.db import models

from ..base.utils.abstracts import TranslatableModel


class FAQCategory(TranslatableModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class FAQ(TranslatableModel):
    LANG_ATTR = "sites__language"
    LANGS_ATTR = "sites__languages"
    sites = models.ManyToManyField("sites.Site")
    # categories = models.ManyToManyField(FAQCategory)
    question = models.CharField(max_length=256)
    answer = models.TextField()

    def __str__(self):
        joined_sites = ", ".join([site.domain for site in self.sites.all()])
        return f"{self.question} [🌐 {joined_sites}]"
