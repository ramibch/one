from auto_prefetch import ForeignKey, Model
from django.contrib.sites.models import Site
from django.db import models
from django.utils.functional import cached_property

from ..links.models import Link
from ..utils.abstracts_and_mixins import PageMixin


class HomePage(Model, PageMixin):
    site = ForeignKey(Site, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    enable_hero_testing = models.BooleanField(default=False)
    allow_field_translation = models.BooleanField(default=False)

    @cached_property
    def active_hero(self):
        return self.hero_set.filter(is_active=True).first()


class Hero(Model):
    homepage = ForeignKey(HomePage, on_delete=models.SET_NULL, null=True)
    headline = models.TextField(max_length=256)
    subheadline = models.TextField(max_length=256)
    cta_link = ForeignKey(Link, on_delete=models.SET_NULL, null=True)
    cta_title = models.CharField(max_length=64, null=True, blank=True)
    cta_new_tab = models.BooleanField(default=False)
    image = models.ImageField(upload_to="homepages/hero/")
    is_active = models.BooleanField()
    allow_field_translation = models.BooleanField(default=False)

    def display_cta_title(self):
        return self.cta_title if self.cta_title else self.cta_link.title

    def __str__(self):
        return f"{self.headline} - {self.homepage}"
