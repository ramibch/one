from urllib.parse import urlparse

from auto_prefetch import ForeignKey, Model, OneToOneField
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from ..base.utils.abstracts import TranslatableModel
from ..links.models import Link

SHOW_CHOICES = (
    ("user", "👤 " + _("For logged user")),
    ("no_user", "🕵🏻 " + _("For anonymous user")),
    ("always", "👁️ " + _("Show always")),
    ("never", "🫣 " + _("Never show")),
)


class NavbarLink(Model):
    order = models.PositiveSmallIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    link = OneToOneField(Link, on_delete=models.CASCADE)
    sites = models.ManyToManyField(Site)
    emoji = models.CharField(max_length=8, null=True, blank=True)
    show_as_emoji = models.BooleanField(default=False)
    show_type = models.CharField(default="always", choices=SHOW_CHOICES, max_length=16)
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
    show_type = models.CharField(default="always", choices=SHOW_CHOICES, max_length=16)
    sites = models.ManyToManyField(Site)

    class Meta(Model.Meta):
        ordering = ("order",)

    def __str__(self) -> str:
        return self.title

    @cached_property
    def display_title(self) -> str:
        return f"{self.emoji} {self.title}" if self.emoji else self.title


class FooterLink(Model):
    order = models.PositiveSmallIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    link = OneToOneField(Link, on_delete=models.CASCADE)
    footer_item = ForeignKey(
        FooterItem, on_delete=models.SET_NULL, null=True, blank=True
    )
    sites = models.ManyToManyField(Site)
    show_type = models.CharField(default="always", choices=SHOW_CHOICES, max_length=16)
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
    sites = models.ManyToManyField(Site)
    url = models.URLField(max_length=256)
    new_tab = models.BooleanField(default=True)
    show_type = models.CharField(default="always", choices=SHOW_CHOICES, max_length=16)

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
