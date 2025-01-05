from auto_prefetch import Model
from django.conf import settings
from django.db import models
from django.urls import reverse_lazy
from django.utils.functional import cached_property

Listing = None  # TODO: rethink how to connect etsy listings


class ProductTag(Model):
    pass


class Product(Model):
    dirname = models.CharField(max_length=128, unique=True)
    image = models.ImageField(upload_to="listings", null=True)
    topics = models.ManyToManyField("base.Topic")
    tags = models.ManyToManyField("products.ProductTag")

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dirname

    def get_listing(self):
        return Listing.objects.get(dirname=self.dirname)

    @cached_property
    def description(self):
        return self.get_listing().get_description()

    def get_absolute_url(self):
        return reverse_lazy("product-detail", kwargs={"slug": self.dirname})

    @cached_property
    def etsy_url(self):
        if (
            self.get_listing().etsy_url != ""
            and self.get_listing().etsy_url is not None
        ):
            return self.get_listing().etsy_url

    @cached_property
    def checkout_url(self):
        return reverse_lazy("product-checkout", kwargs={"id": self.id})

    @cached_property
    def page_url(self):
        return self.get_absolute_url()

    @cached_property
    def full_page_url(self):
        return settings.WEBSITE_URL + self.page_url

    @cached_property
    def price(self):
        return self.get_listing().price

    @cached_property
    def price_in_cents(self):
        return int(self.price * 100)

    @cached_property
    def title(self):
        return self.get_listing().title

    @cached_property
    def keywords(self):
        return self.get_listing().keywords

    @cached_property
    def listing_type(self):
        return self.get_listing().listing_type
