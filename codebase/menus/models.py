from auto_prefetch import ForeignKey, Model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from urllib.parse import urlparse

from ..articles.models import Article
from ..pages.models import Page

URL_PATHS = (
    # name, display name
    ("home", _("Home")),
    ("search", _("Search")),
    ("sitemap", _("Sitemap")),
    ("article-list", _("Articles")),
)


class MenuItem(Model):
    title = models.CharField(max_length=64)
    emoji = models.CharField(max_length=8, null=True, blank=True)
    order = models.IntegerField(default=0)
    show_in_navbar = models.BooleanField(default=True)
    show_in_footer = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

    class Meta(Model.Meta):
        ordering = ("order",)


class PageLink(Model):
    order = models.IntegerField(default=0)
    menu_item = ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True, blank=True)
    emoji = models.CharField(max_length=8, null=True, blank=True)
    custom_title = models.CharField(max_length=128, null=True, blank=True)
    django_url_path = models.CharField(blank=True, null=True, max_length=32, choices=URL_PATHS)
    page = ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    article = ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    external_url = models.URLField(max_length=256, null=True, blank=True)
    new_tab = models.BooleanField(default=False)
    show_in_navbar = models.BooleanField(default=False)
    show_as_emoji = models.BooleanField(default=False)

    class Meta(Model.Meta):
        ordering = ("order",)

    def clean(self):
        are_links = tuple(obj is not None for obj in (self.django_url_path, self.page, self.article, self.external_url))
        if are_links.count(True) != 1:
            raise ValidationError(_("One link must be entered."), code="invalid")

        if self.external_url and self.custom_title is None:
            raise ValidationError(_("Enter a custom title if an external url is entered."), code="invalid")

        if self.show_as_emoji and self.emoji is None:
            raise ValidationError(_("Insert an emoji if you want to show it as emoji."), code="invalid")

    @cached_property
    def url(self):
        if self.django_url_path:
            return reverse_lazy(self.django_url_path)

        for obj in (self.page, self.article):
            if getattr(obj, "url", None):
                return obj.url
        return self.external_url

    @cached_property
    def text_only_title(self):

        if self.custom_title:
            return self.custom_title

        if self.django_url_path:
            return self.get_django_url_path_display()

        for page_obj in (self.page, self.article):
            if getattr(page_obj, "title", None):
                return page_obj.title

    @cached_property
    def full_title(self):
        return f"{self.emoji} {self.text_only_title}" if self.emoji else self.text_only_title

    @cached_property
    def title(self):
        return self.emoji if self.show_as_emoji else self.full_title


    def __str__(self):
        return self.full_title



class SocialMediaLink(Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    url = models.URLField(max_length=128, null=True, blank=True)
    new_tab = models.BooleanField(default=True)
    show = models.BooleanField(default=True)

    @cached_property
    def platform(self):
        return urlparse(self.url).netloc.replace("www.", "").split(".")[0]

    def __str__(self):
        return self.title

