import secrets
from datetime import timedelta

from auto_prefetch import ForeignKey
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from one.bot import Bot
from one.db import OneModel

from .utils import get_linkedin_access_from_code


class LinkedinAuthorType(models.TextChoices):
    PERSON = "person", _("Person")
    ORGANIZATION = "organization", _("Organization")


class LinkedinAuth(OneModel):
    state = models.CharField(max_length=128, default=secrets.token_hex)
    code = models.TextField(blank=True, null=True)
    access_token = models.TextField(blank=True, null=True, editable=False)
    expires_at = models.DateTimeField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True, editable=False)
    refresh_token_expires_at = models.DateTimeField(blank=True, null=True)
    scope = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"[{self.pk}] {self.state}"

    def update_values(self, access_data:dict, code:str|None=None):
        """
        access_data = {
                      "access_token": <access_token>,
                      "expires_in": 86400,
                      "refresh_token": <refresh_token>,
                      "refresh_token_expires_in": 439200,
                      "scope":"r_basicprofile"
                      }
        """

        if code:
            self.code = code
        
        log = [f"🔄 Updating LinkedinAuth ({self.pk})"]

        if "access_token" in access_data:
            self.access_token = access_data["access_token"]
            log.append("✅ access_token received")
        else:
            log.append("⚠️ access_token missing")

        if "refresh_token" in access_data:
            self.refresh_token = access_data["refresh_token"]
            log.append("✅ refresh_token received")
        else:
            log.append("⚠️ refresh_token missing")

        if "expires_in" in access_data:
            self.expires_at = timezone.now() + timedelta(seconds=access_data["expires_in"])
            log.append(f"✅ expires_in set to {self.expires_at}")
        else:
            log.append("⚠️ expires_in missing")

        if "refresh_token_expires_in" in access_data:
            self.refresh_token_expires_at = timezone.now() + timedelta(seconds=access_data["refresh_token_expires_in"])
            log.append(f"✅ refresh_token_expires_in set to {self.refresh_token_expires_at}")
        else:
            log.append("⚠️ refresh_token_expires_in missing")

        if "scope" in access_data:
            self.scope = access_data["scope"]
            log.append("✅ scope set")
        else:
            log.append("⚠️ scope missing")

        self.save()
        Bot.to_admin("\n".join(log))


class LinkedinChannel(OneModel):
    auth = ForeignKey(LinkedinAuth, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    author_type = models.CharField(max_length=32, choices=LinkedinAuthorType)

    def __str__(self) -> str:
        return self.name