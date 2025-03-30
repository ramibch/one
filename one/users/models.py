from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property


class User(AbstractUser):
    asked_to_verify_email = models.BooleanField(default=False)
    when_asked_to_verify = models.DateTimeField(blank=True)
    country_code = models.CharField(max_length=8, null=True)
    language = models.CharField(max_length=8, choices=settings.LANGUAGES, null=True)
    sites = models.ManyToManyField("sites.Site", blank=True)

    def __str__(self) -> str:
        return f"User ({self.username} - {self.email})"

    @cached_property
    def delete_account_url(self):
        return reverse("account_delete", kwargs={"id": self.id})

    @cached_property
    def fullname(self):
        return self.first_name + " " + self.last_name

    @cached_property
    def display_name(self):
        if self.first_name not in ("", None):
            return self.first_name
        return self.username
