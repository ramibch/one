from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property


class User(AbstractUser):
    asked_to_verify_email = models.BooleanField(default=False)
    country_code = models.CharField(max_length=8, null=True)

    @cached_property
    def delete_account_url(self):
        return reverse("account_delete", kwargs={"id": self.id})

    @cached_property
    def fullname(self):
        return self.first_name + " " + self.last_name

    def __str__(self) -> str:
        return f"User ({self.username} - {self.email})"
