from auto_prefetch import ForeignKey, Model, OneToOneField
from django.contrib.auth import get_user_model
from django.contrib.gis.geoip2 import GeoIP2
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from ..base import Countries
from ..base.utils.telegram import Bot

User = get_user_model()


class GeoInfo(Model):
    accuracy_radius = models.SmallIntegerField(null=True)  # 1000
    city = models.CharField(max_length=64, null=True)  # "Mountain View"
    continent_code = models.CharField(max_length=64, null=True)  # "NA"
    continent_name = models.CharField(max_length=64, null=True)  # "North America"
    country_code = models.CharField(max_length=64, null=True)  # "US"
    country_name = models.CharField(max_length=64, null=True)  # "United States"
    is_in_european_union = models.BooleanField(null=True)  # False
    latitude = models.FloatField(null=True)  # 37.419200897216797
    longitude = models.FloatField(null=True)  # -122.05740356445312
    metro_code = models.SmallIntegerField(null=True)  # 807
    postal_code = models.CharField(max_length=64, null=True)  # "94043"
    region_code = models.CharField(max_length=64, null=True)  # "CA"
    region_name = models.CharField(max_length=64, null=True)  # "California"
    time_zone = models.CharField(max_length=64, null=True)  # "America/Los_Angeles"
    dma_code = models.SmallIntegerField(null=True)  # 807
    region = models.CharField(max_length=32, null=True)  # "CA"

    def __str__(self):
        return f"{self.postal_code} {self.city}, {self.country_name}"


class Client(Model):
    user = ForeignKey(User, null=True, on_delete=models.SET_NULL)
    country = models.CharField(max_length=2, choices=Countries, default="CH")
    site = ForeignKey("sites.Site", null=True, on_delete=models.SET_NULL)
    geoinfo = OneToOneField(GeoInfo, null=True, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    is_blocked = models.BooleanField(default=False)
    user_agent = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.ip_address

    @classmethod
    def dummy_object(cls):
        return cls.objects.get_or_create(ip_address="10.10.10.10")[0]

    @cached_property
    def country_data(self) -> dict:
        try:
            return GeoIP2().country(self.ip_address)
        except Exception as e:
            Bot.to_admin(f"Client: GeoIP2 country error: {e}")
            return {}

    @cached_property
    def city_data(self) -> dict:
        try:
            return GeoIP2().city(self.ip_address)
        except Exception as e:
            Bot.to_admin(f"GeoInfo: GeoIP2 city error: {e}")
            return {}

    def update_values(self):
        # Country
        if self.country_data != {}:
            self.country = self.country_data.get("country_code")

        # Geo info
        if self.city_data != {} and self.geoinfo is None:
            self.geoinfo = GeoInfo.objects.create(**self.city_data)

        self.save()


class Request(Model):
    """
    Model to register request data
    Check this repo for inspiration:
    https://github.com/django-request/django-request/blob/master/request/models.py

    """

    client = ForeignKey(Client, on_delete=models.CASCADE)
    path = models.CharField(max_length=256, db_index=True)
    method = models.CharField(default="GET", max_length=7)
    get = models.TextField(null=True)
    post = models.TextField(null=True)
    ref = models.CharField(max_length=255, null=True, db_index=True)
    headers = models.TextField(null=True)
    status_code = models.PositiveSmallIntegerField(default=200)
    time = models.DateTimeField(_("time"), default=timezone.now, db_index=True)

    def save_from_midddleware(self, request, response):
        self.client = request.client
        self.path = request.path[:255]
        self.method = request.method
        self.get = request.GET
        self.post = request.POST
        self.ref = request.GET.get("ref", "")[:256]
        self.headers = request.headers
        self.status_code = response.status_code
        self.save()

    def __str__(self):
        time = self.time.strftime("%Y-%m-%d %H:%M")
        return f"[{time}] {self.method} " f"{self.path} {self.status_code}"
