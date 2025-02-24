from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property

from ..base import Languages


class User(AbstractUser):
    asked_to_verify_email = models.BooleanField(default=False)
    country_code = models.CharField(max_length=8, null=True)
    language = models.CharField(max_length=8, choices=Languages.choices, null=True)
    sites = models.ManyToManyField("sites.Site", blank=True)
    possible_spam = models.BooleanField(default=False)

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
