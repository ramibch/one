from auto_prefetch import ForeignKey, Model
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from django.utils.functional import cached_property

from one.base.utils.abstracts import (
    BaseSubmoduleFolder,
    TranslatableModel,
)

User = get_user_model()


class Product(TranslatableModel, BaseSubmoduleFolder, submodule="products"):
    """Product model as folder"""

    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    summary = models.TextField(blank=True, null=True)
    etsy_id = models.PositiveIntegerField(null=True, blank=True)
    etsy_url = models.URLField(max_length=256, null=True, blank=True)
    price = models.FloatField(default=1.0)
    topics = models.ManyToManyField("base.Topic")

    def get_absolute_url(self):
        return reverse_lazy("product-detail", kwargs={"slug": self.dirname})

    @cached_property
    def checkout_url(self):
        return reverse_lazy("product-checkout", kwargs={"id": self.id})


def get_file_path(obj, filename: str):
    return f"products/{obj._meta.model_name}/{filename}"


class ProductFile(Model):
    """Product file model"""

    product = ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to=get_file_path)

    def __str__(self):
        return self.name


class ProductImage(Model):
    product = ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to=get_file_path)
