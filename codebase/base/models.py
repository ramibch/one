from auto_prefetch import ForeignKey, Manager, Model
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone, translation
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from ..articles.models import Article
from ..products.models import Product
from . import Language
from .utils.abstracts import TranslatableModel

User = get_user_model()


class TrafficManager(Manager):
    def create_from_request_reponse_and_ip(self, request, response, ip):
        return self.create(
            user=request.user if request.user.is_authenticated else None,
            site=request.site,
            path=request.path,
            method=request.method,
            get=request.GET,
            post=request.POST,
            ref=request.GET.get("ref", None),
            headers=request.headers,
            country_code=request.country.code,
            status_code=response.status_code,
            ip=ip,
            ip_blocked=False,
        )


class Traffic(Model):
    """
    Model to register traffic data
    Check this repo for inspiration:
    https://github.com/django-request/django-request/blob/master/request/models.py

    """

    # Request info
    site = ForeignKey("sites.Site", null=True, on_delete=models.SET_NULL)  # type: ignore
    user = ForeignKey(User, null=True, on_delete=models.SET_NULL)  # type: ignore
    path = models.CharField(max_length=255, db_index=True)
    method = models.CharField(default="GET", max_length=7)
    get = models.TextField(null=True)
    post = models.TextField(null=True)
    ref = models.CharField(max_length=255, null=True, db_index=True)
    headers = models.TextField(null=True)
    country_code = models.CharField(max_length=8, null=True, db_index=True)
    ip = models.GenericIPAddressField(_("ip address"), null=True)

    # Response info
    status_code = models.PositiveSmallIntegerField(default=200)

    # Others
    time = models.DateTimeField(_("time"), default=timezone.now, db_index=True)
    ip_blocked = models.BooleanField(default=False)

    objects: TrafficManager = TrafficManager()

    def __str__(self):
        return f"[{self.time}] {self.method} " f"{self.path} {self.status_code}"


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

    def get_default_language(self):
        return settings.LANGUAGE_CODE

    def get_rest_languages(self) -> set:
        return set(Language.values)
