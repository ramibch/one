from django.db import models
from django.utils import timezone
from etsyv3 import EtsyAPI

from ..base.utils.abstracts import SingletonModel


def etsy_refresh_save(access_token, refresh_token, expires_at):
    # It's intended to be a 'neat' way to handle refreshes
    etsy = Etsy.load()
    etsy.access_token = access_token
    etsy.refresh_token = refresh_token
    etsy.expires_at = timezone.make_aware(expires_at, timezone.get_fixed_timezone(0))
    etsy.save()


class Etsy(SingletonModel):
    name = models.CharField(max_length=32)
    shop_id = models.PositiveIntegerField(
        default=39982277,
        help_text="On your shop's main page and while logged in, (using a PC) right click on View Page Source and search for shop_id",
    )
    keystring = models.CharField(
        max_length=256,
        help_text="An Etsy App API Key keystring for the app.",
    )
    redirect_uri = models.URLField(
        max_length=200,
        default="https://ramiboutas.com/auths/etsy/callback",
        help_text="A callback URL your app uses to receive the authorization code",
    )
    scopes = models.CharField(
        max_length=256,
        default="listings_d, listings_r, listings_w, profile_r, profile_w, shops_r, shops_w, transactions_r",
        help_text="The scopes your application requires to use specific endpoints",
    )
    state = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text="A state string, similar to a strong password, which protects against Cross-site request forgery exploits.",
    )
    code_verifier = models.CharField(
        help_text="A code verifier for code exchange (PKCE)",
        max_length=256,
        null=True,
        blank=True,
    )
    code = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text="An OAuth authorization code required to request an OAuth token",
    )
    access_token = models.CharField(max_length=256, null=True, blank=True)
    refresh_token = models.CharField(max_length=256, null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.keystring})"

    def get_api_client(self):
        return EtsyAPI(
            keystring=self.keystring,
            token=self.access_token,
            refresh_token=self.refresh_token,
            expiry=timezone.make_naive(
                self.expires_at,
                timezone=timezone.get_fixed_timezone(0),
            ),
            refresh_save=etsy_refresh_save,
        )
