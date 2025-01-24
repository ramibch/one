from django.conf import settings
from django.db import models

from one.base.utils.abstracts import TranslatableModel


class Shop(TranslatableModel):
    general_listing_description = models.TextField()

    def get_default_language(self) -> str:
        return settings.LANGUAGE_CODE

    def get_rest_languages(self) -> set:
        return settings.LANGUAGE_CODES_WITHOUT_DEFAULT


class Listing(TranslatableModel):
    shop = models.ManyToManyField(Shop)
    price = models.FloatField(default=1.0)
    tags = models.ManyToManyField("base.Topic")
    title = models.CharField(max_length=128)
    summary = models.TextField()
    etsy_id = models.PositiveIntegerField(null=True, blank=True)
    etsy_url = models.URLField(max_length=256, null=True, blank=True)
    # product_folder =

    def get_default_language(self) -> str:
        return settings.LANGUAGE_CODE

    def get_rest_languages(self) -> set:
        return settings.LANGUAGE_CODES_WITHOUT_DEFAULT
