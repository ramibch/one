from auto_prefetch import ForeignKey, Model
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from .animations import (
    AnimationDelay,
    AnimationRepeat,
    AnimationSpeed,
    AnimationType,
    AttentionSeekers,
)

User = get_user_model()


class SearchTerm(Model):
    query = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    client = ForeignKey("clients.Client", null=True, on_delete=models.SET_NULL)
    site = ForeignKey("sites.Site", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.query


class ContactMessage(Model):
    client = ForeignKey(
        "clients.Client",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    site = ForeignKey(
        "sites.Site",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(_("Your name"), max_length=128)
    email = models.EmailField(_("Email address"), max_length=128)
    message = models.TextField(_("Message"), max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name}  <{self.email}>"


class Animation(Model):
    animation_type = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        default=AnimationType.VANILLA,
        choices=AnimationType.choices,
    )
    name = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        default=AttentionSeekers.FLASH,
        choices=AttentionSeekers.choices,
    )
    repeat = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        default=AnimationRepeat.ONE,
        choices=AnimationRepeat.choices,
    )
    speed = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=AnimationSpeed.choices,
    )
    delay = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=AnimationDelay.choices,
    )
