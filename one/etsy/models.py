import re

from auto_prefetch import ForeignKey, Model, OneToOneField
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.files.storage import storages
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils import translation
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from etsyv3.models.file_request import UploadListingFileRequest, UploadListingImageRequest
from etsyv3.models.listing_request import CreateDraftListingRequest, CreateListingTranslationRequest

from one.base.utils.abstracts import TranslatableModel
from one.base.utils.db_fields import ChoiceArrayField
from one.base.utils.telegram import Bot

from .enums import ListingType, Scopes, TaxonomyID, WhenMade, WhoMade
from .etsy_api import ExtendedEtsyAPI

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
        unique=True,
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
        return reverse("etsy_code") + f"?keystring={self.keystring}"

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

    class Meta(Model.Meta):
        ordering = ["-id"]

    def __str__(self):
        return f"[{self.etsy_user_id}] {self.app}"

    def get_api_client(self) -> ExtendedEtsyAPI:
        return ExtendedEtsyAPI(
            keystring=self.app.keystring,
            token=self.access_token,
            refresh_token=self.refresh_token,
            expiry=self.expires_at,
            refresh_save=auth_refresh_save,
        )


class UserShop(Model):
    user_shop_auth = ForeignKey(UserShopAuth, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name



class UserListing(Model):
    user_shop_auth = ForeignKey(UserShopAuth, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveSmallIntegerField(
        default=999,
        validators=[MinValueValidator(0), MaxValueValidator(999)],
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    who_made = models.CharField(
        max_length=32,
        default=WhoMade.I_DID,
        choices=WhoMade.choices,
    )
    when_made = models.CharField(
        max_length=32,
        default=WhenMade.YEARS_2020_2025,
        choices=WhenMade.choices,
    )
    taxonomy_id = models.PositiveIntegerField(
        default=TaxonomyID.DIGITAL_PRINTS,
        choices=TaxonomyID.choices,
    )
    shop_section_id = models.PositiveIntegerField(null=True, blank=True)

    tags = models.TextField(null=True)

    is_personalizable = models.BooleanField(
        null=True,
        blank=True,
        help_text=_("This listing is personalizable or not."),
    )
    personalization_is_required = models.BooleanField(
        null=True,
        blank=True,
        help_text=_(
            "Listing requires personalization or not. "
            "Will only change if is_personalizable is 'true'."
        ),
    )
    personalization_char_count_max = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text=_(
            "It represents the maximum length for the personalization message "
            "entered by the buyer. Will only change if is_personalizable is 'true'."
        ),
    )
    personalization_instructions = models.TextField(
        null=True,
        blank=True,
        help_text=_(
            "It represents  instructions for the buyer to enter the personalization. "
            "Will only change if is_personalizable is 'true'."
        ),
    )
    is_customizable = models.BooleanField(
        null=True,
        blank=True,
        help_text=_(
            "When true, a buyer may contact the seller for a customized order. "
            "The default value is true when a shop accepts custom orders. "
            "Does not apply to shops that do not accept custom orders."
        ),
    )
    should_auto_renew = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        help_text=_("Renews or not a listing for four months upon expiration."),
    )
    is_taxable = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        help_text=_("Tax rates apply or not to this listing at checkout."),
    )
    listing_type = models.CharField(
        max_length=32,
        default=ListingType.DOWNLOAD,
        choices=ListingType,
        help_text=_(
            "An enumerated type string that indicates whether "
            "the listing is physical or a digital download."
        ),
    )

    # Response or read-only fields
    state = models.CharField(max_length=32, null=True)
    creation_timestamp = models.PositiveBigIntegerField(null=True)
    created_timestamp = models.PositiveBigIntegerField(null=True)
    ending_timestamp = models.PositiveBigIntegerField(null=True)
    original_creation_timestamp = models.PositiveBigIntegerField(null=True)
    last_modified_timestamp = models.PositiveBigIntegerField(null=True)
    updated_timestamp = models.PositiveBigIntegerField(null=True)
    state_timestamp = models.PositiveBigIntegerField(null=True)
    featured_rank = models.PositiveIntegerField(null=True)
    url = models.URLField(null=True)
    num_favorers = models.PositiveIntegerField(null=True)
    non_taxable = models.BooleanField(null=True)
    is_private = models.BooleanField(null=True)
    language = models.CharField(max_length=32, null=True)


def get_file_path(obj, filename: str):
    return f"etsy/users/{obj.listing.id}/{obj._meta.model_name}/{filename}"


class UserListingFile(Model):
    listing = ForeignKey(UserListing, on_delete=models.CASCADE)
    listing_file_id = models.PositiveBigIntegerField(null=True)
    file = models.FileField(upload_to=get_file_path, storage=storages["private"])
    rank = models.PositiveSmallIntegerField(default=1)

    # Response or read-only fields
    filename = models.CharField(max_length=256, null=True)
    filesize = models.CharField(max_length=256, null=True)
    size_bytes = models.PositiveBigIntegerField(null=True)
    filetype = models.CharField(max_length=128, null=True)
    create_timestamp = models.PositiveBigIntegerField(null=True)
    created_timestamp = models.PositiveBigIntegerField(null=True)

    @cached_property
    def name(self):
        return self.file.name.split("/")[-1]


class UserListingImage(Model):
    listing = ForeignKey(UserListing, on_delete=models.CASCADE)
    file = models.ImageField(upload_to=get_file_path, storage=storages["private"])
    listing_image_id = models.PositiveBigIntegerField(null=True)
    rank = models.PositiveSmallIntegerField(default=1)
    name = models.CharField(max_length=256, null=True)
    overwrite = models.BooleanField(default=False)
    is_watermarked = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=250, null=True)

    # Response or read-only fields
    hex_code = models.TextField(null=True)
    red = models.PositiveSmallIntegerField(null=True)
    green = models.PositiveSmallIntegerField(null=True)
    blue = models.PositiveSmallIntegerField(null=True)
    hue = models.PositiveSmallIntegerField(null=True)
    saturation = models.PositiveSmallIntegerField(null=True)
    brightness = models.PositiveSmallIntegerField(null=True)
    is_black_and_white = models.BooleanField(default=False)
    creation_tsz = models.PositiveBigIntegerField(null=True)  # No idea what is this
    created_timestamp = models.PositiveBigIntegerField(null=True)
    url_75x75 = models.URLField(max_length=512, null=True)
    url_170x135 = models.URLField(max_length=512, null=True)
    url_570xN = models.URLField(max_length=512, null=True)
    url_fullxfull = models.URLField(max_length=512, null=True)
    full_height = models.PositiveIntegerField(null=True)
    full_width = models.PositiveIntegerField(null=True)
