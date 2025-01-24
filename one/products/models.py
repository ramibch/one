from auto_prefetch import Model
from django.db import models
from django.urls import reverse_lazy
from django.utils.functional import cached_property

Listing = None  # TODO: rethink how to connect etsy listings


from auto_prefetch import ForeignKey
from django.contrib.auth import get_user_model

from one.base.utils.abstracts import (
    BaseSubmoduleFolder,
)

from ..base import Languages
from ..base.utils.db_fields import ChoiceArrayField

User = get_user_model()


class Product(BaseSubmoduleFolder, submodule="products"):
    """Product model as folder"""

    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    topics = models.ManyToManyField("base.Topic")
    languages = ChoiceArrayField(
        models.CharField(max_length=4, choices=Languages),
        default=list,
        blank=True,
    )

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
