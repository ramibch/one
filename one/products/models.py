from auto_prefetch import ForeignKey, Model
from django.contrib.auth import get_user_model
from django.core.files.storage import storages
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from one.base.utils.abstracts import (
    BaseSubmoduleFolder,
    TranslatableModel,
)

User = get_user_model()


class Product(TranslatableModel, BaseSubmoduleFolder, submodule="products"):
    """Product model as folder"""

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
    topics = models.ManyToManyField("base.Topic")

    def get_absolute_url(self):
        return reverse_lazy("product-detail", kwargs={"slug": self.slug})

    @cached_property
    def checkout_url(self):
        return reverse_lazy("product-checkout", kwargs={"id": self.id})

    @cached_property
    def file_paths(self):
        base = self.folder_path / "files"
        return [base / fobj.name for fobj in self.productfile_set.all()]

    @cached_property
    def image_paths(self):
        base = self.folder_path / "images"
        return [base / fobj.name for fobj in self.productfile_set.all()]


def get_file_path(obj, filename: str):
    return f"products/{obj._meta.model_name}/{filename}"


class ProductFile(Model):
    """Product file model"""

    product = ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to=get_file_path, storage=storages["private"])

    def __str__(self):
        return self.name


class ProductImage(Model):
    product = ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to=get_file_path)

    def __str__(self):
        return self.name
