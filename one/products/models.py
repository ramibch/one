from auto_prefetch import ForeignKey, Manager, OneToOneField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.storage import storages
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

from one.bot import Bot
from one.choices import Topics
from one.db import BaseSubmoduleFolder, ChoiceArrayField, OneModel, TranslatableModel
from one.etsy.enums import ListingType, TaxonomyID, WhenMade, WhoMade

User = get_user_model()


class ProductManager(Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_draft=False)


class Product(TranslatableModel, BaseSubmoduleFolder, submodule="products"):
    """Product model as folder"""

    LANG_ATTR = "language"
    LANGS_ATTR = "languages"
    I18N_SLUGIFY_FROM = "title"

    language = models.CharField(
        max_length=4,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
    )
    languages = ChoiceArrayField(
        models.CharField(max_length=8, choices=settings.LANGUAGES),
        default=list,
        blank=True,
    )

    topics = ChoiceArrayField(
        models.CharField(max_length=16, choices=Topics),
        default=list,
        blank=True,
    )

    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=1.0)
    discount_percentage = models.SmallIntegerField(
        default=90,
        verbose_name=_("Discount in percentage"),
        help_text=_("It is applied to the country with the lowest GDP per capita."),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    is_draft = models.BooleanField(default=True)

    objects = ProductManager()

    def get_absolute_url(self):
        return reverse_lazy("product-detail", kwargs={"slug": self.slug})

    @cached_property
    def checkout_url(self):
        return reverse_lazy("product-checkout", kwargs={"id": self.id})

    @cached_property
    def file_paths(self):
        base = self.folder_path / "files"
        return [base / fobj.name for fobj in self.productfile_set.all()]  # type: ignore

    @cached_property
    def image_paths(self):
        base = self.folder_path / "images"
        return [base / fobj.name for fobj in self.productimage_set.all()]  # type: ignore


def get_file_path(obj, filename: str):
    return f"products/{obj._meta.model_name}/{filename}"


class ProductFile(OneModel):
    """Product file model"""

    product = ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to=get_file_path, storage=storages["private"])

    def __str__(self):
        return self.name


class ProductImage(OneModel):
    product = ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to=get_file_path)

    def __str__(self):
        return self.name


class EtsyShop(TranslatableModel):
    LANG_ATTR = "language"
    LANGS_ATTR = "languages"
    language = models.CharField(
        max_length=4,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
    )
    languages = ChoiceArrayField(
        models.CharField(max_length=8, choices=settings.LANGUAGES),
        default=list,
        blank=True,
    )
    user_shop_auth = OneToOneField("etsy.EtsyAuth", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=64, default="Shop example")
    generic_listing_description = models.TextField()

    topics = ChoiceArrayField(
        models.CharField(max_length=16, choices=Topics),
        default=list,
        blank=True,
    )

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


# TODO:
# class Tag(OneModel):
#     name = models.CharField()


class EtsyListing(OneModel):
    include_generic_description = models.BooleanField(default=True)

    shop = ForeignKey(EtsyShop, on_delete=models.CASCADE)
    product = ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        default=999,
        validators=[MinValueValidator(0), MaxValueValidator(999)],
    )
    price = models.FloatField(default=1.0)
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

    listing_type = models.CharField(
        max_length=32,
        default=ListingType.DOWNLOAD,
        choices=ListingType.choices,
    )

    # tags =
    # TODO: add tags

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
        if self.include_generic_description:
            return (
                f"{self.product.description}\n\n{self.shop.generic_listing_description}"
            )
        else:
            return self.product.description

    def get_tags(self) -> list[str]:
        # TODO: REmove
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

        translation.activate(self.shop.language)
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
        for lang in self.shop.get_languages_without_default():
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
