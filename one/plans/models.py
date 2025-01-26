from auto_prefetch import Model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.functional import cached_property
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from one.base.utils.mixins import PageMixin


class Plan(Model, PageMixin):
    title = models.CharField(max_length=256, editable=False)
    description = models.CharField(max_length=128, null=True)
    slug = models.SlugField(max_length=128, unique=True, editable=False)
    price_min = MoneyField(
        max_digits=6, decimal_places=2, default_currency="EUR", default=Money(5, "EUR")
    )
    price_max = MoneyField(
        max_digits=6, decimal_places=2, default_currency="EUR", default=Money(50, "EUR")
    )

    def get_absolute_url(self):
        return reverse_lazy("plan_detail", kwargs={"slug": self.slug})

    def get_price(self, country_code="CH"):
        pass

    @cached_property
    def detail_url(self):
        return reverse("plan_detail", kwargs={"id": self.id})

    @cached_property
    def checkout_url(self):
        return reverse("plan_checkout", kwargs={"id": self.id})

    def clean(self):
        if self.price_min.currency != self.price_max.currency:
            raise ValidationError("price_min and price_max must have the same currency")
        if self.price_min > self.price_max:
            raise ValidationError("The field price_min must be smaller than price_max")
        super().clean()
