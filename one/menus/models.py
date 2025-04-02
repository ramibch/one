from urllib.parse import urlparse

from auto_prefetch import ForeignKey, Model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from one.base.utils.abstracts import TranslatableModel


class ShowTypes(models.TextChoices):
    USER = "user", "👤 " + _("For logged user")
    NO_USER = "no_user", "🕵🏻 " + _("For anonymous user")
    ALWAYS = "always", "👁️ " + _("Show always")
    NEVER = "never", "🫣 " + _("Never show")


class NavbarLink(Model):
    sites = models.ManyToManyField("sites.Site")
    link = ForeignKey(
        "links.Link",
        on_delete=models.CASCADE,
    )
    emoji = models.CharField(max_length=8, null=True, blank=True)
    show_as_emoji = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
    )
    show_type = models.CharField(
        default=ShowTypes.ALWAYS,
        choices=ShowTypes,
        max_length=16,
    )
    new_tab = models.BooleanField(default=False)

    class Meta(Model.Meta):
        ordering = ("order",)

    def __str__(self):
        return self.title

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
    LANG_ATTR = "sites__language"
    LANGS_ATTR = "sites__languages"
    sites = models.ManyToManyField("sites.Site")
    emoji = models.CharField(
        max_length=8,
        null=True,
        blank=True,
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(8),
        ],
    )

    show_type = models.CharField(
        default=ShowTypes.ALWAYS,
        choices=ShowTypes,
        max_length=16,
    )
    title = models.CharField(max_length=64)

    class Meta(Model.Meta):
        ordering = ("order",)

    def __str__(self) -> str:
        return self.title

    @cached_property
    def display_title(self) -> str:
        return f"{self.emoji} {self.title}" if self.emoji else self.title


class FooterLink(Model):
    sites = models.ManyToManyField("sites.Site")
    link = ForeignKey(
        "links.Link",
        on_delete=models.CASCADE,
    )
    footer_item = ForeignKey(
        "menus.FooterItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
    )
    show_type = models.CharField(
        default=ShowTypes.ALWAYS,
        choices=ShowTypes,
        max_length=16,
    )
    new_tab = models.BooleanField(default=False)

    class Meta(Model.Meta):
        ordering = ("order",)

    def __str__(self):
        return f"FooterLink {self.link}"

    @cached_property
    def display_title(self) -> str:
        return self.link.title


class SocialMediaLink(Model):
    sites = models.ManyToManyField("sites.Site")
    url = models.URLField(max_length=256)
    new_tab = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
    )
    show_type = models.CharField(
        default=ShowTypes.ALWAYS,
        choices=ShowTypes,
        max_length=16,
    )

    class Meta(Model.Meta):
        ordering = ("order",)

    def __str__(self):
        return f"SocialMediaLink {self.url}"

    @cached_property
    def static_icon_url(self) -> str:
        """
        svg location of the platform logo

        https://icons8.com/icons

        """
        return f"img/social/small/{self.platform}.svg"

    @cached_property
    def platform(self) -> str:
        return urlparse(self.url).netloc.replace("www.", "").split(".")[0]
