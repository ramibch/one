from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat
from django.urls import reverse
from django.utils.functional import cached_property


class User(AbstractUser):
    asked_to_verify_email = models.BooleanField(db_default=False)
    when_asked_to_verify = models.DateTimeField(blank=True, null=True)
    full_name = models.GeneratedField(
        expression=Concat("first_name", Value(" "), "last_name"),
        output_field=models.CharField(max_length=300),
        db_persist=True,
    )
    country_code = models.CharField(
        max_length=8,
        blank=True,
        null=True,
    )
    language = models.CharField(
        max_length=8,
        choices=settings.LANGUAGES,
        blank=True,
        null=True,
    )

    sites = models.ManyToManyField(
        "sites.Site",
        blank=True,
    )

    def __str__(self) -> str:
        return f"User ({self.username} - {self.email})"

    @cached_property
    def delete_account_url(self):
        return reverse("account_delete", kwargs={"id": self.id})

    @cached_property
    def display_name(self):
        if self.first_name not in ("", None):
            return self.first_name
        return self.username
