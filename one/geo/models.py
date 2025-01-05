from auto_prefetch import Model
from django.db import models


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

    class Meta(Model.Meta):
        unique_together = ["latitude", "longitude"]

    def __str__(self):
        return f"{self.postal_code} {self.city}, {self.country_name}"
