from auto_prefetch import ForeignKey, Model, OneToOneField
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.files.storage import storages
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from etsyv3.models.file_request import (
    UploadListingFileRequest,
    UploadListingImageRequest,
)
from etsyv3.models.listing_request import (
    CreateDraftListingRequest,
    UpdateListingRequest,
)

from one.base.utils.db import ChoiceArrayField, update_model_from_dict
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


def auth_refresh_save(access_token, refresh_token, expires_at):
    """
    This function is intended to be a 'neat' way to handle refreshes

    https://developer.etsy.com/documentation/essentials/authentication/#step-3-request-an-access-token

    """

    user_id = access_token.split(".")[0]
    etsy_auth = EtsyAuth.objects.filter(etsy_user_id=user_id).last()
    if etsy_auth:
        etsy_auth.access_token = access_token
        etsy_auth.refresh_token = refresh_token
        etsy_auth.expires_at = expires_at
        etsy_auth.save()
    else:
        Bot.to_admin(f"Etsy: Failed to save tokens, user_id = {user_id}")


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

    is_commercial = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f"{self.name} ({self.keystring})"

    def get_absolute_url(self):
        return reverse("etsy_code") + f"?keystring={self.keystring}"

    @cached_property
    def request_auth_url(self):
        return self.get_absolute_url()


class EtsyAuth(Model):
    app = ForeignKey(App, on_delete=models.CASCADE, null=True)
    user = ForeignKey(User, on_delete=models.CASCADE, null=True)
    etsy_user_id = models.PositiveBigIntegerField(null=True)
    shop_id = models.PositiveBigIntegerField(null=True)
    state = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text=(
            "A state string, similar to a strong password, "
            "which protects against Cross-site request forgery exploits."
        ),
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

    def get_api_client(self) -> ExtendedEtsyAPI:
        return ExtendedEtsyAPI(
            keystring=self.app.keystring,
            token=self.access_token,
            refresh_token=self.refresh_token,
            expiry=self.expires_at,
            refresh_save=auth_refresh_save,
        )

    def get_shop_dict(self):
        api = self.get_api_client()
        return api.get_shop(shop_id=self.shop_id)


class Shop(Model):
    etsy_auth = OneToOneField(EtsyAuth, on_delete=models.CASCADE)
    shop_id = models.PositiveBigIntegerField(primary_key=True)
    shop_name = models.CharField(max_length=128)
    user_id = models.PositiveBigIntegerField()
    create_date = models.PositiveBigIntegerField(null=True)
    created_timestamp = models.PositiveBigIntegerField(null=True)
    title = models.CharField(max_length=256)
    announcement = models.CharField(max_length=256, null=True)
    currency_code = models.CharField(max_length=8)
    is_vacation = models.BooleanField(default=False)
    vacation_message = models.CharField(max_length=512, null=True)
    sale_message = models.CharField(max_length=512, null=True)
    digital_sale_message = models.CharField(max_length=512, null=True)
    update_date = models.PositiveBigIntegerField(null=True)
    updated_timestamp = models.PositiveBigIntegerField(null=True)
    listing_active_count = models.PositiveIntegerField(null=True)
    digital_listing_count = models.PositiveIntegerField(null=True)
    login_name = models.CharField(max_length=256, null=True)
    accepts_custom_requests = models.BooleanField(null=True)
    vacation_autoreply = models.CharField(max_length=512, null=True)
    url = models.URLField(max_length=256, null=True)
    image_url_760x100 = models.URLField(max_length=512, null=True)
    num_favorers = models.PositiveIntegerField(null=True)
    languages = ArrayField(
        models.CharField(max_length=16), default=list, blank=True, null=True
    )
    icon_url_fullxfull = models.URLField(max_length=512, null=True)
    is_using_structured_policies = models.BooleanField(null=True)
    has_onboarded_structured_policies = models.BooleanField(null=True)
    include_dispute_form_link = models.BooleanField(null=True)
    is_direct_checkout_onboarded = models.BooleanField(null=True)
    is_etsy_payments_onboarded = models.BooleanField(null=True)
    is_opted_in_to_buyer_promise = models.BooleanField(null=True)
    is_calculated_eligible = models.BooleanField(null=True)
    is_shop_us_based = models.BooleanField(null=True)
    transaction_sold_count = models.PositiveBigIntegerField(null=True)
    shipping_from_country_iso = models.CharField(null=True)
    shop_location_country_iso = models.CharField(null=True)
    policy_welcome = models.TextField(null=True)
    policy_payment = models.TextField(null=True)
    policy_shipping = models.TextField(null=True)
    policy_refunds = models.TextField(null=True)
    policy_additional = models.TextField(null=True)
    policy_seller_info = models.TextField(null=True)
    policy_update_date = models.PositiveBigIntegerField(null=True)
    policy_has_private_receipt_info = models.BooleanField(null=True)
    has_unstructured_policies = models.BooleanField(null=True)
    policy_privacy = models.TextField(null=True)
    review_average = models.FloatField(null=True)
    review_count = models.PositiveIntegerField(null=True)
    etsy_dict = models.JSONField(null=True)

    def update_from_etsy(self):
        try:
            shop_dict = self.etsy_auth.get_shop_dict()
            self.etsy_dict = shop_dict
            update_model_from_dict(self, shop_dict, save=True)
        except Exception as e:
            Bot.to_admin(f"Not possible to update Etsy Shop\n{e}")

    def __str__(self):
        return self.shop_name


class Listing(Model):
    etsy_auth = ForeignKey(EtsyAuth, on_delete=models.CASCADE, null=True)
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
    taxonomy_id = models.PositiveIntegerField(default=TaxonomyID.DIGITAL_PRINTS)
    shop_section_id = models.PositiveIntegerField(null=True, blank=True)

    tags = models.TextField(null=True)

    is_personalizable = models.BooleanField(
        default=False,
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
    is_supply = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        help_text=_(
            "When true, tags the listing as a supply product, "
            "else indicates that it's a finished product. "
            "Helps buyers locate the listing under the Supplies heading. "
            "Requires 'who_made' and 'when_made'."
        ),
    )

    # Response or read-only fields
    listing_id = models.PositiveBigIntegerField(null=True)
    state = models.CharField(max_length=32, null=True)
    creation_timestamp = models.PositiveBigIntegerField(null=True)
    created_timestamp = models.PositiveBigIntegerField(null=True)
    ending_timestamp = models.PositiveBigIntegerField(null=True)
    original_creation_timestamp = models.PositiveBigIntegerField(null=True)
    last_modified_timestamp = models.PositiveBigIntegerField(null=True)
    updated_timestamp = models.PositiveBigIntegerField(null=True)
    state_timestamp = models.PositiveBigIntegerField(null=True)
    featured_rank = models.IntegerField(null=True)
    url = models.URLField(null=True)
    num_favorers = models.PositiveIntegerField(null=True)
    non_taxable = models.BooleanField(null=True)
    is_private = models.BooleanField(null=True)
    language = models.CharField(max_length=32, null=True)
    etsy_dict = models.JSONField(null=True)

    feedback_fields = (
        "listing_id",
        "state",
        "creation_timestamp",
        "created_timestamp",
        "ending_timestamp",
        "original_creation_timestamp",
        "last_modified_timestamp",
        "updated_timestamp",
        "state_timestamp",
        "featured_rank",
        "url",
        "num_favorers",
        "non_taxable",
        "is_private",
        "language",
        "etsy_dict",
    )

    def __str__(self):
        return self.title

    def update_in_etsy(self):
        if self.listing_id is None:
            Bot.to_admin(f"⚠️ Not possible to update listing ({self.id}).")
            return

        api_client = ExtendedEtsyAPI(
            keystring=self.etsy_auth.app.keystring,
            token=self.etsy_auth.access_token,
            refresh_token=self.etsy_auth.refresh_token,
            expiry=self.etsy_auth.expires_at,
            refresh_save=auth_refresh_save,
        )
        shop_id = self.etsy_auth.shop_id
        request_listing = UpdateListingRequest(
            title=self.title,
            description=self.description,
            tags=self.tags,
        )
        try:
            api_client.update_listing(
                shop_id=shop_id,
                listing_id=self.listing_id,
                listing=request_listing,
            )
        except Exception as e:
            Bot.to_admin(f"⚠️ Error by updating listing ({self.id}).\n{e}")

    def upload_to_etsy(self):
        # api_client = self.etsy_auth.get_api_client()
        api_client = ExtendedEtsyAPI(
            keystring=self.etsy_auth.app.keystring,
            token=self.etsy_auth.access_token,
            refresh_token=self.etsy_auth.refresh_token,
            expiry=self.etsy_auth.expires_at,
            refresh_save=auth_refresh_save,
        )

        shop_id = self.etsy_auth.shop_id

        request_listing = CreateDraftListingRequest(
            quantity=self.quantity,
            title=self.title,
            description=self.description,
            price=self.price,
            who_made=self.who_made,
            when_made=self.when_made,
            taxonomy_id=self.taxonomy_id,
            listing_type=self.listing_type,
            tags=self.tags,
        )

        response = api_client.create_draft_listing(
            shop_id=shop_id, listing=request_listing
        )
        self.etsy_dict = response
        for field in self.feedback_fields:
            setattr(self, field, response.get(field))
        self.save()

        # Images
        for image_obj in self.images.all():
            request_image = UploadListingImageRequest(
                image_bytes=image_obj.file.storage.open(
                    image_obj.file.name, "rb"
                ).read(),
                rank=image_obj.rank,
            )
            image_obj.etsy_dict = api_client.upload_listing_image(
                shop_id=shop_id,
                listing_id=self.listing_id,
                listing_image=request_image,
            )
            update_model_from_dict(image_obj, image_obj.etsy_dict, save=True)

        # Files
        for file_obj in self.files.all():
            request_file = UploadListingFileRequest(
                file_bytes=file_obj.file.storage.open(file_obj.file.name, "rb").read(),
                name=file_obj.name,
                rank=file_obj.rank,
            )
            file_obj.etsy_dict = api_client.upload_listing_file(
                shop_id=shop_id,
                listing_id=self.listing_id,
                listing_file=request_file,
            )
            update_model_from_dict(file_obj, file_obj.etsy_dict, save=True)


def get_file_path(obj, filename: str):
    return f"etsy/users/{obj.listing.id}/{obj._meta.model_name}/{filename}"


class ListingFile(Model):
    listing = ForeignKey(Listing, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to=get_file_path, storage=storages["private"])
    rank = models.PositiveSmallIntegerField(default=1)

    # Response or read-only fields
    listing_file_id = models.PositiveBigIntegerField(null=True)
    filename = models.CharField(max_length=256, null=True)
    filesize = models.CharField(max_length=256, null=True)
    size_bytes = models.PositiveBigIntegerField(null=True)
    filetype = models.CharField(max_length=128, null=True)
    create_timestamp = models.PositiveBigIntegerField(null=True)
    created_timestamp = models.PositiveBigIntegerField(null=True)
    etsy_dict = models.JSONField(null=True)

    feedback_fields = (
        "listing_file_id",
        "filename",
        "filesize",
        "size_bytes",
        "filetype",
        "create_timestamp",
        "created_timestamp",
        "etsy_dict",
    )

    @cached_property
    def name(self):
        return self.file.name.split("/")[-1]


class ListingImage(Model):
    listing = ForeignKey(Listing, on_delete=models.CASCADE, related_name="images")
    file = models.ImageField(upload_to=get_file_path, storage=storages["private"])
    rank = models.PositiveSmallIntegerField(default=1)
    overwrite = models.BooleanField(default=False, null=True)
    is_watermarked = models.BooleanField(default=False, null=True)
    alt_text = models.CharField(max_length=250, null=True)

    # Response or read-only fields
    listing_image_id = models.PositiveBigIntegerField(null=True)
    hex_code = models.TextField(null=True)
    red = models.PositiveSmallIntegerField(null=True)
    green = models.PositiveSmallIntegerField(null=True)
    blue = models.PositiveSmallIntegerField(null=True)
    hue = models.PositiveSmallIntegerField(null=True)
    saturation = models.PositiveSmallIntegerField(null=True)
    brightness = models.PositiveSmallIntegerField(null=True)
    is_black_and_white = models.BooleanField(default=False, null=True)
    creation_tsz = models.PositiveBigIntegerField(null=True)  # No idea what is this
    created_timestamp = models.PositiveBigIntegerField(null=True)
    url_75x75 = models.URLField(max_length=512, null=True)
    url_170x135 = models.URLField(max_length=512, null=True)
    url_570xN = models.URLField(max_length=512, null=True)
    url_fullxfull = models.URLField(max_length=512, null=True)
    full_height = models.PositiveIntegerField(null=True)
    full_width = models.PositiveIntegerField(null=True)
    etsy_dict = models.JSONField(null=True)
    feedback_fields = (
        "listing_image_id",
        "hex_code",
        "red",
        "green",
        "blue",
        "hue",
        "saturation",
        "brightness",
        "is_black_and_white",
        "creation_tsz",
        "created_timestamp",
        "url_75x75",
        "url_170x135",
        "url_570xN",
        "url_fullxfull",
        "full_height",
        "full_width",
        "etsy_dict",
    )

    @cached_property
    def name(self):
        return self.file.name.split("/")[-1]
