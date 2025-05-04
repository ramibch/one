import googlemaps
from auto_prefetch import Model
from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.db import models

from one.base.utils.telegram import Bot


class GeoInfo(Model):
    accuracy_radius = models.SmallIntegerField(null=True)
    city = models.CharField(max_length=128, null=True)
    continent_code = models.CharField(max_length=64, null=True)
    continent_name = models.CharField(max_length=128, null=True)
    country_code = models.CharField(max_length=64, null=True)
    country_name = models.CharField(max_length=64, null=True)
    is_in_european_union = models.BooleanField(null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    metro_code = models.SmallIntegerField(null=True)
    postal_code = models.CharField(max_length=64, null=True)
    region_code = models.CharField(max_length=64, null=True)
    region_name = models.CharField(max_length=128, null=True)
    time_zone = models.CharField(max_length=128, null=True)
    dma_code = models.SmallIntegerField(null=True)
    region = models.CharField(max_length=32, null=True)
    location = PointField(blank=True, null=True)

    class Meta(Model.Meta):
        unique_together = ["latitude", "longitude"]

    def __str__(self):
        return f"{self.postal_code} {self.city}, {self.country_name}"


class GoogleGeoInfo(Model):
    address = models.TextField(unique=True)
    payload = models.JSONField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    location = PointField(blank=True, null=True)

    def __str__(self):
        return self.address

    def update_attrs(self):
        if self.payload:
            payload = self.payload
        else:
            gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
            payload = gmaps.geocode(self.address)
            self.payload = payload

        try:
            self.latitude = payload[0]["geometry"]["location"]["lat"]
            self.longitude = payload[0]["geometry"]["location"]["lng"]
            self.location = Point(self.longitude, self.latitude)
        except Exception as e:
            Bot.to_admin(f"Unable to get lat o lon from {self.address}: {e}")

        self.save()
