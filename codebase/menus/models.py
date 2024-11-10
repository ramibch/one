from urllib.parse import urlparse

from auto_prefetch import ForeignKey, Model
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from ..utils.abstracts_and_mixins import AbstractLinkModel
from ..utils.constants import SHOW_CHOICES


class NavbarLink(AbstractLinkModel):
    order = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    emoji = models.CharField(max_length=8, null=True, blank=True)
    show_as_emoji = models.BooleanField(default=False)
    site = models.ManyToManyField(Site)
    show_type = models.CharField(default="always", choices=SHOW_CHOICES, max_length=16)

    class Meta(AbstractLinkModel.Meta):
        ordering = ("order",)

    @cached_property
    def title(self):
        return f"{self.emoji} {super().title}" if self.emoji else super().title

    @cached_property
    def display_title(self):
        return self.emoji if self.show_as_emoji else self.title

    def clean_show_as_emoji(self):
        if self.show_as_emoji and not self.emoji:
            raise ValidationError(_("Insert an emoji if you want to show it as emoji."), code="invalid")


class FooterItem(Model):
    order = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(8)])
    emoji = models.CharField(max_length=8, null=True, blank=True)
    title = models.CharField(max_length=64)
    show_type = models.CharField(default="always", choices=SHOW_CHOICES, max_length=16)
    site = models.ManyToManyField(Site)
    allow_field_translation = models.BooleanField(default=False)

    class Meta(Model.Meta):
        ordering = ("order",)

    def __str__(self) -> str:
        return self.title

    @cached_property
    def display_title(self) -> str:
        return f"{self.emoji} {super().title}" if self.emoji else super().title


class FooterLink(AbstractLinkModel):
    order = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    footer_item = ForeignKey(FooterItem, on_delete=models.SET_NULL, null=True, blank=True)
    site = models.ManyToManyField(Site)
    show_type = models.CharField(default="always", choices=SHOW_CHOICES, max_length=16)

    class Meta(AbstractLinkModel.Meta):
        ordering = ("order",)

    @cached_property
    def display_title(self) -> str:
        return super().title


class SocialMediaLink(Model):
    order = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    url = models.URLField(max_length=256)
    new_tab = models.BooleanField(default=True)
    show_type = models.CharField(default="always", choices=SHOW_CHOICES, max_length=16)
    site = models.ManyToManyField(Site)
    allow_field_translation = models.BooleanField(default=False)

    @cached_property
    def static_icon_url(self) -> str:
        return f"img/social/small/{self.platform}.svg"

    class Meta(Model.Meta):
        ordering = ("order",)

    def __str__(self) -> str:
        if self.url:
            return self.url
        return getattr(self, f"url_{settings.LANGUAGE_CODE}")

    @cached_property
    def platform(self) -> str:
        return urlparse(self.url).netloc.replace("www.", "").split(".")[0]
