from auto_prefetch import ForeignKey, Model, OneToOneField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse_lazy
from django.utils import translation
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from etsyv3.models.file_request import (
    UploadListingFileRequest,
    UploadListingImageRequest,
)
from etsyv3.models.listing_request import (
    CreateDraftListingRequest,
    CreateListingTranslationRequest,
)

from one.base.utils.abstracts import TranslatableModel
from one.base.utils.db_fields import ChoiceArrayField
from one.base.utils.telegram import Bot

from .api import ExtendedEtsyAPI
from .enums import ListingType, Scopes, TaxonomyID, WhenMade, WhoMade

User = get_user_model()


def get_default_scopes():
    return [
        "listings_d",
        "listings_r",
        "listings_w",
        "profile_r",
        "profile_w",
        "shops_r",
        "shops_w",
        "transactions_r",
    ]


class App(Model):
    name = models.CharField(max_length=32)
    keystring = models.CharField(
        max_length=256,
        help_text="An Etsy App API Key keystring for the app.",
    )
    redirect_uri = models.URLField(
        max_length=200,
        default="https://ramib.ch/etsy/callback",
        help_text="A callback URL your app uses to receive the authorization code",
    )
    scopes = ChoiceArrayField(
        models.CharField(max_length=16, choices=Scopes),
        default=get_default_scopes,
        help_text="The scopes your application requires to use specific endpoints",
    )

    def __str__(self):
        return f"{self.name} ({self.keystring})"

    def get_absolute_url(self):
        return reverse_lazy("etsy_code", kwargs={"id": self.id})

    @cached_property
    def request_auth_url(self):
        return self.get_absolute_url()


def auth_refresh_save(access_token, refresh_token, expires_at):
    """
    This function is intended to be a 'neat' way to handle refreshes

    https://developer.etsy.com/documentation/essentials/authentication/#step-3-request-an-access-token

    """

    user_id = access_token.split(".")[0]
    app = UserShopAuth.objects.filter(etsy_user_id=user_id).last()
    if app:
        app.access_token = access_token
        app.refresh_token = refresh_token
        app.expires_at = expires_at
        app.save()
    else:
        Bot.to_admin(f"Etsy: Failed to save tokens, user_id = {user_id}")


class UserShopAuth(Model):
    app = ForeignKey(App, on_delete=models.CASCADE, null=True)
    user = ForeignKey(User, on_delete=models.CASCADE, null=True)
    etsy_user_id = models.PositiveBigIntegerField(null=True)
    shop_id = models.PositiveBigIntegerField(null=True)
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
    scopes = ChoiceArrayField(
        models.CharField(max_length=16, choices=Scopes),
        default=get_default_scopes,
        help_text="The scopes your application requires to use specific endpoints",
    )
    access_token = models.CharField(max_length=256, null=True, blank=True)
    refresh_token = models.CharField(max_length=256, null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"[{self.etsy_user_id}] {self.app}"

    def get_api_client(self) -> type[ExtendedEtsyAPI]:
        return ExtendedEtsyAPI(
            keystring=self.app.keystring,
            token=self.access_token,
            refresh_token=self.refresh_token,
            expiry=self.expires_at,
            refresh_save=auth_refresh_save,
        )


class Shop(TranslatableModel):
    user_shop_auth = OneToOneField(UserShopAuth, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=64, default="Shop example")
    generic_listing_description = models.TextField()
    topics = models.ManyToManyField("base.Topic")
    price_percentage = models.SmallIntegerField(
        default=150,
        verbose_name=_("Price percentace"),
        help_text=_("Percent to apply to Etsy listing price."),
        validators=[MinValueValidator(50), MaxValueValidator(300)],
    )
    etsy_payload = models.JSONField(null=True, blank=True)

    @cached_property
    def api_client(self):
        if self.user_shop_auth:
            return self.user_shop_auth.get_api_client()
        raise ValueError

    @cached_property
    def shop_id(self):
        return self.user_shop_auth.shop_id

    def request_and_save_payload(self):
        self.etsy_payload = self.api_client.get_shop(self.shop_id)
        self.save()

    def __str__(self):
        return self.name


class Listing(Model):
    shop = ForeignKey(Shop, on_delete=models.CASCADE)
    user_shop_auth = ForeignKey(UserShopAuth, on_delete=models.CASCADE, null=True)
    product = ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        default=999,
        validators=[MinValueValidator(0), MaxValueValidator(999)],
    )
    price = models.FloatField(default=1.0)
    who_made = models.CharField(
        max_length=32,
        default=WhoMade.I_DID,
        choices=WhoMade,
    )
    when_made = models.CharField(
        max_length=32,
        default=WhenMade.YEARS_2020_2025,
        choices=WhenMade,
    )
    taxonomy_id = models.PositiveIntegerField(
        default=TaxonomyID.DIGITAL_PRINTS,
        choices=TaxonomyID,
    )

    listing_type = models.CharField(
        max_length=32,
        default=ListingType.DOWNLOAD,
        choices=ListingType,
    )

    # Attrs after response
    response = models.JSONField(null=True, blank=True)
    listing_id = models.PositiveIntegerField(null=True, blank=True)
    url = models.URLField(max_length=256, null=True, blank=True)
    state = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return f"[{self.shop}] {self.product}"

    def get_title(self) -> str:
        return self.product.title

    def get_description(self) -> str:
        return f"{self.product.description}\n\n{self.shop.generic_listing_description}"

    def get_tags(self) -> list[str]:
        return list(self.product.topics.all().values_list("name", flat=True))

    @cached_property
    def api_client(self):
        return self.user_shop_auth.get_api_client()

    @cached_property
    def shop_id(self):
        return self.user_shop_auth.shop_id

    def upload_to_etsy(self):
        if self.listing_id:
            Bot.to_admin(f"Listing already in Etsy:\n{self.product}\n{self.url}")
            return

        api_client = self.api_client
        shop_id = self.shop_id

        translation.activate(self.shop.default_language)
        request_listing = CreateDraftListingRequest(
            quantity=self.quantity,
            title=self.get_title(),
            description=self.get_description(),
            price=self.price,
            who_made=self.who_made,
            when_made=self.when_made,
            taxonomy_id=self.taxonomy_id,
            listing_type=self.listing_type,
            tags=self.get_tags(),
        )

        response = api_client.create_draft_listing(
            shop_id=shop_id, listing=request_listing
        )

        self.listing_id = response.get("listing_id")
        self.url = response.get("url")
        self.state = response.get("state")
        self.response = response
        self.save()

        translation.deactivate()

        # Images
        for rank, path in enumerate(self.product.image_paths, start=1):
            with open(path, "rb") as f:
                api_client.upload_listing_image(
                    shop_id=shop_id,
                    listing_id=self.listing_id,
                    listing_image=UploadListingImageRequest(
                        image_bytes=f.read(), rank=rank
                    ),
                )

        # Files
        for path in self.product.file_paths:
            with open(path, "rb") as f:
                api_client.upload_listing_file(
                    shop_id=shop_id,
                    listing_id=self.listing_id,
                    listing_file=UploadListingFileRequest(
                        file_bytes=f.read(), name=path.name
                    ),
                )

        # Translations
        for lang in self.shop.languages_without_default:
            with translation.override(lang):
                listing_translation = CreateListingTranslationRequest(
                    title=self.get_title(),
                    description=self.get_description(),
                    tags=self.get_tags(),
                )
                api_client.create_listing_translation(
                    shop_id=self.shop.shop_id,
                    listing_id=self.listing_id,
                    language=lang,
                    listing_translation=listing_translation,
                )
