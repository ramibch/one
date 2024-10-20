from auto_prefetch import ForeignKey, Model
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from ..articles.models import Article
from ..pages.models import Page


class NavbarItem(Model):
    LOCATIONS = (("left", _("Left")), ("right", _("Right")))

    title = models.CharField(max_length=64)
    location = models.CharField(max_length=8, choices=LOCATIONS, default="right")
    order = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title

    class Meta(Model.Meta):
        ordering = ("order",)


class FooterItem(Model):
    title = models.CharField(max_length=64)
    order = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title

    class Meta(Model.Meta):
        ordering = ("order",)


class PageLink(Model):
    navbar_item = ForeignKey(NavbarItem, on_delete=models.CASCADE, null=True, blank=True)
    footer_item = ForeignKey(FooterItem, on_delete=models.CASCADE, null=True, blank=True)
    page = ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    article = ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    custom_title = models.CharField(max_length=128, null=True, blank=True)
    external_url = models.URLField(max_length=128, null=True, blank=True)
    target_blank = models.BooleanField(default=False)

    @cached_property
    def url(self):
        for obj in (self.page, self.article):
            if getattr(obj, "url", None):
                return obj.url
        return self.external_url

    @cached_property
    def title(self):
        pass

    def __str__(self):
        return self.title
