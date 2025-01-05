from urllib.parse import urlparse

from auto_prefetch import ForeignKey, Model
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from ..base.utils.abstracts import TranslatableModel
from ..links.models import Link


class ShowTypes(models.TextChoices):
    USER = "user", "👤 " + _("For logged user")
    NO_USER = "no_user", "🕵🏻 " + _("For anonymous user")
    ALWAYS = "always", "👁️ " + _("Show always")
    NEVER = "never", "🫣 " + _("Never show")


class NavbarLink(Model):
    order = models.PositiveSmallIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    link = ForeignKey(Link, on_delete=models.CASCADE)
    sites = models.ManyToManyField("sites.Site")
    emoji = models.CharField(max_length=8, null=True, blank=True)
    show_as_emoji = models.BooleanField(default=False)
    show_type = models.CharField(
        default=ShowTypes.ALWAYS, choices=ShowTypes.choices, max_length=16
    )
    new_tab = models.BooleanField(default=False)

    class Meta(Model.Meta):
        ordering = ("order",)

    @cached_property
    def title(self):
        return f"{self.emoji} {self.link.title}" if self.emoji else self.link.title

    @cached_property
    def display_title(self):
        return self.emoji if self.show_as_emoji else self.title

    def clean_show_as_emoji(self):
        if self.show_as_emoji and self.emoji is None:
            raise ValidationError(
                _("Insert an emoji if you want to show it as emoji."), code="invalid"
            )


class FooterItem(TranslatableModel):
    order = models.PositiveSmallIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(8)]
    )
    emoji = models.CharField(max_length=8, null=True, blank=True)
    title = models.CharField(max_length=64)
    show_type = models.CharField(
        default=ShowTypes.ALWAYS, choices=ShowTypes.choices, max_length=16
    )
    sites = models.ManyToManyField("sites.Site")

    class Meta(Model.Meta):
        ordering = ("order",)

    def __str__(self) -> str:
        return self.title

    @cached_property
    def display_title(self) -> str:
        return f"{self.emoji} {self.title}" if self.emoji else self.title

    def get_default_language(self) -> str:
        return settings.LANGUAGE_CODE

    def get_rest_languages(self) -> set:
        return {lang for site in self.sites.all() for lang in site.rest_languages}


class FooterLink(Model):
    order = models.PositiveSmallIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    link = ForeignKey(Link, on_delete=models.CASCADE)
    footer_item = ForeignKey(
        "menus.FooterItem", on_delete=models.SET_NULL, null=True, blank=True
    )
    sites = models.ManyToManyField("sites.Site")
    show_type = models.CharField(
        default=ShowTypes.ALWAYS, choices=ShowTypes.choices, max_length=16
    )
    new_tab = models.BooleanField(default=False)

    class Meta(Model.Meta):
        ordering = ("order",)

    @cached_property
    def display_title(self) -> str:
        return self.link.title


class SocialMediaLink(Model):
    order = models.PositiveSmallIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    sites = models.ManyToManyField("sites.Site")
    url = models.URLField(max_length=256)
    new_tab = models.BooleanField(default=True)
    show_type = models.CharField(
        default=ShowTypes.ALWAYS, choices=ShowTypes.choices, max_length=16
    )

    class Meta(Model.Meta):
        ordering = ("order",)

    def __str__(self) -> str:
        return self.url

    @cached_property
    def static_icon_url(self) -> str:
        return f"img/social/small/{self.platform}.svg"

    @cached_property
    def platform(self) -> str:
        return urlparse(self.url).netloc.replace("www.", "").split(".")[0]


def generate_navbar_link_list(*, link_list: list, show_type: str, start_order: int):
    """Utility function to get a list of NavbarLink objects"""
    new_links = []
    for index, link in enumerate(link_list, start=start_order):
        new_links.append(NavbarLink(link=link, show_type=show_type, order=index))
    return new_links


def generate_footer_link_list(*, link_list: list):
    """Utility function to get a list of FooterLink objects"""
    new_links = []
    for index, link in enumerate(link_list, start=1):
        new_links.append(FooterLink(link=link, order=index))
    return new_links


def create_initial_menu_objects(sites) -> bool:
    """
    Utility function to create initial menu objects for specified sites.

    Returns `True` if objects were created, otherwise `False`.

    """

    if (
        NavbarLink.objects.filter(sites__in=sites).exists()
        or FooterLink.objects.filter(sites__in=sites).exists()
    ):
        return False

    search = Link.objects.get_or_create(django_url_path="search")[0]
    article_list = Link.objects.get_or_create(django_url_path="article_list")[0]
    login = Link.objects.get_or_create(django_url_path="account_login")[0]
    logout = Link.objects.get_or_create(django_url_path="account_signup")[0]
    dashboard = Link.objects.get_or_create(django_url_path="user_dashboard")[0]
    home = Link.objects.get_or_create(django_url_path="home")[0]

    always_links = (search, article_list)
    no_user_links = (login, logout)
    user_links = (dashboard,)

    # Navbar links
    navbar_link_list = generate_navbar_link_list(
        link_list=always_links,
        show_type=ShowTypes.ALWAYS,
        start_order=1,
    )
    navbar_link_list += generate_navbar_link_list(
        link_list=no_user_links,
        show_type=ShowTypes.NO_USER,
        start_order=4,
    )
    navbar_link_list += generate_navbar_link_list(
        link_list=user_links,
        show_type=ShowTypes.USER,
        start_order=6,
    )

    navbar_links = NavbarLink.objects.bulk_create(navbar_link_list)
    for navbar_link in navbar_links:
        navbar_link.sites.set(sites)

    # Footer links

    footer_link_list = generate_footer_link_list(link_list=[home, article_list, search])
    footer_links = FooterLink.objects.bulk_create(footer_link_list)

    for footer_link in footer_links:
        footer_link.sites.set(sites)

    return True
