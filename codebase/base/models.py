from auto_prefetch import ForeignKey, Model
from django.db import models
from django.utils.functional import cached_property

from ..articles.models import Article
from ..pages.models import Page


class MenuItem(Model):
    title = models.CharField(max_length=64)
    order = models.IntegerField(default=0)
    show_in_navbar = models.BooleanField(default=True)
    show_in_footer = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

    class Meta(Model.Meta):
        ordering = ("order",)


class PageLink(Model):
    menu_item = ForeignKey(MenuItem, on_delete=models.CASCADE)
    page = ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    article = ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    external_title = models.CharField(max_length=128, null=True, blank=True)
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
        for obj in (self.page, self.article):
            if getattr(obj, "title", None):
                return obj.title
        return self.external_title

    def __str__(self):
        return self.title
