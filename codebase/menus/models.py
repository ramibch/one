from auto_prefetch import ForeignKey, Model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

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
    emoji = models.CharField(max_length=8, null=True, blank=True)
    emoji_as_title = models.BooleanField(default=False)
    custom_title = models.CharField(max_length=128, null=True, blank=True)
    menu_item = ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True, blank=True)
    show_in_navbar = models.BooleanField(default=False)
    url_path = models.CharField(blank=True, null=True, max_length=32, choices=URL_PATHS)
    page = ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    article = ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    external_url = models.URLField(max_length=128, null=True, blank=True)
    new_tab = models.BooleanField(default=False)

    @cached_property
    def url(self):
        if self.url_path:
            return reverse_lazy(self.url_path)

        for obj in (self.page, self.article):
            if getattr(obj, "url", None):
                return obj.url
        return self.external_url

    @cached_property
    def title(self):
        if self.emoji and self.custom_title:
            return f"{self.emoji} {self.custom_title}"

        if self.custom_title :
            return self.custom_title

        if self.url_path:
            return self.get_url_path_display()

        for obj in (self.page, self.article):
            if getattr(obj, "title", None):
                return obj.title

    def clean(self):
        are_links = tuple(obj is not None for obj in (self.url_path, self.page, self.article, self.external_url))
        if are_links.count(True) != 1:
            raise ValidationError(_("One link must be entered."), code="invalid")

        if self.external_url and self.custom_title is None:
            raise ValidationError(_("Enter a custom title if an external url is entered."), code="invalid")

        if self.emoji_as_title and self.emoji is None:
            raise ValidationError(_("Emoji needs to be entered."), code="invalid")

        if self.emoji_as_title and self.menu_item is not None:
            raise ValidationError(_("Emoji as title requires no menu item."), code="invalid")


    def __str__(self):
        return self.title


    class Meta(Model.Meta):
        ordering = ("order",)



class SocialMediaLink(Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    url = models.URLField(max_length=128, null=True, blank=True)
    new_tab = models.BooleanField(default=False)
    show = models.BooleanField(default=True)


    def __str__(self):
        return self.title

