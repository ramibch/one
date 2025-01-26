from django.db import models

from one.base.utils.abstracts import TranslatableModel


class Shop(TranslatableModel):
    general_listing_description = models.TextField()
    products = models.ManyToManyField("products.Product", blank=True)
