from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from django.utils import translation
from django.utils.functional import cached_property
from django.utils.text import slugify

from ..articles.models import Article
from ..products.models import Product
from .utils.abstracts import TranslatableModel

User = get_user_model()


class Topic(TranslatableModel):
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=32, unique=True, blank=True, db_index=True)
    is_public = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def title(self):
        return self.name

    @cached_property
    def related_articles(self):
        return Article.objects.filter(public=True, topic=self)

    @cached_property
    def related_products(self):
        return Product.objects.filter(topics__id=self.id)[:6]

    def get_absolute_url(self):
        return reverse_lazy("topic-detail", kwargs={"slug": self.slug})

    @cached_property
    def url(self):
        return self.get_absolute_url()

    @cached_property
    def article_count(self):
        return Article.objects.filter(topic=self).count()

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        for lang in settings.LANGUAGE_CODES:
            with translation.override(lang):
                setattr(self, f"slug_{lang}", slugify(self.name))
        super().save(*args, **kwargs)
