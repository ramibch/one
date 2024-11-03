from urllib.parse import urlparse

from auto_prefetch import ForeignKey, Model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from ..articles.models import Article
from ..pages.models import Page
from ..plans.models import Plan

DJANGO_URL_PATHS = (
    ("home", _("Home")),
    ("search", _("Search")),
    ("sitemap", _("Sitemap")),
    ("article_list", _("Articles")),
    ("plan_list", _("Plans")),
    ("account_login", _("Sign In")),
    ("account_signup", _("Sign Up")),
    ("user_dashboard", _("Account")),
)


SHOW_TYPES = (
    ("user", "👤 " + _("For logged user")),
    ("no_user", "🕵🏻 " + _("For anonymous user")),
    ("always", "👁️ " + _("Show always")),
    ("never", "🫣 " + _("Never show")),
)


class AbstractLink(Model):
    order = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    custom_title = models.CharField(max_length=128, null=True, blank=True)
    django_url_path = models.CharField(blank=True, null=True, max_length=32, choices=DJANGO_URL_PATHS)
    page = ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    plan = ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True)
    article = ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    external_url = models.URLField(max_length=256, null=True, blank=True)
    new_tab = models.BooleanField(default=False)
    show_type = models.CharField(default="always", choices=SHOW_TYPES, max_length=16)

    class Meta(Model.Meta):
        abstract = True
        ordering = ("order",)

    @cached_property
    def link_fields(self):
        return (self.django_url_path, self.page, self.plan, self.article, self.external_url)

    def clean(self):
        super().clean()
        are_links = tuple(obj is not None for obj in self.link_fields)
        if are_links.count(True) != 1:
            raise ValidationError(_("One link must be entered."), code="invalid")

        if self.external_url and self.custom_title is None:
            raise ValidationError(_("Enter a custom title if an external url is entered."), code="invalid")

    @cached_property
    def url(self):
        if self.django_url_path:
            return reverse_lazy(self.django_url_path)

        for obj in (self.page, self.plan, self.article):
            if getattr(obj, "url", None):
                return obj.url

        return self.external_url

    @cached_property
    def text_only_title(self):
        if self.custom_title:
            return self.custom_title

        if self.django_url_path:
            return self.get_django_url_path_display()

        for page_obj in (self.page, self.plan, self.article):
            if getattr(page_obj, "title", None):
                return page_obj.title

    def __str__(self):
        return self.title


class NavbarLink(AbstractLink):
    emoji = models.CharField(max_length=8, null=True, blank=True)
    show_as_emoji = models.BooleanField(default=False)

    @cached_property
    def title(self):
        return f"{self.emoji} {self.text_only_title}" if self.emoji else self.text_only_title

    @cached_property
    def display_title(self):
        return self.emoji if self.show_as_emoji else self.title

    def clean(self):
        super().clean()
        if self.show_as_emoji and self.emoji is None:
            raise ValidationError(_("Insert an emoji if you want to show it as emoji."), code="invalid")


class FooterItem(Model):
    order = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(12)])
    emoji = models.CharField(max_length=8, null=True, blank=True)
    title = models.CharField(max_length=64)
    show_type = models.CharField(default="always", choices=SHOW_TYPES, max_length=16)

    def __str__(self) -> str:
        return self.title

    class Meta(Model.Meta):
        ordering = ("order",)

    @cached_property
    def display_title(self):
        return f"{self.emoji} {self.title}" if self.emoji else self.title


class FooterLink(AbstractLink):
    footer_item = ForeignKey(FooterItem, on_delete=models.SET_NULL, null=True, blank=True)

    @cached_property
    def title(self):
        return self.text_only_title

    @cached_property
    def display_title(self):
        return self.title


class SocialMediaLink(Model):
    order = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    url = models.URLField(max_length=256)
    new_tab = models.BooleanField(default=True)
    show_type = models.CharField(default="always", choices=SHOW_TYPES, max_length=16)

    @cached_property
    def platform(self):
        return urlparse(self.url).netloc.replace("www.", "").split(".")[0]

    def __str__(self):
        return self.url
