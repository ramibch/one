from auto_prefetch import ForeignKey, Model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from one.base.utils.abstracts import TranslatableModel


class Shop(TranslatableModel):
    general_listing_description = models.TextField()
    topics = models.ManyToManyField("base.Topic")
    overprice_percentage = models.SmallIntegerField(
        default=150,
        verbose_name=_("Overprice percentace"),
        help_text=_("Percent to apply to Etsy listing price."),
        validators=[MinValueValidator(100), MaxValueValidator(300)],
    )


class TaxonomyID(models.IntegerChoices):
    DIGITAL_PRINTS = 2078, _("Digital prints")


class Listing(Model):
    shop = ForeignKey("etsy.Shop", on_delete=models.CASCADE)
    product = ForeignKey("products.Product", on_delete=models.CASCADE)
    etsy_id = models.PositiveIntegerField(null=True, blank=True)
    etsy_url = models.URLField(max_length=256, null=True, blank=True)
    price = models.FloatField(default=1.0)
    taxonomy_id = models.PositiveIntegerField(
        default=TaxonomyID.DIGITAL_PRINTS,
        choices=TaxonomyID,
    )
