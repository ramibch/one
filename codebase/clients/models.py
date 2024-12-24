from auto_prefetch import ForeignKey, Model
from django.contrib.auth import get_user_model
from django.contrib.gis.geoip2 import GeoIP2
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from ..base.utils.telegram import Bot

User = get_user_model()


class Country(Model):
    code = models.CharField(max_length=8, null=True, db_index=True)

    def __str__(self):
        return self.code


class Client(Model):
    user = ForeignKey(User, null=True, on_delete=models.SET_NULL)
    country = ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    site = ForeignKey("sites.Site", null=True, on_delete=models.SET_NULL)
    ip_address = models.GenericIPAddressField()
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.ip_address

    @cached_property
    def country_data(self) -> dict | None:
        try:
            return GeoIP2().country(self.ip_address)
        except Exception as e:
            Bot.to_admin(f"Client coutrny error: {e}")
            return {}

    def get_country_object(self):
        code = self.country_data.get("country_code")
        return Country.objects.get_or_create(code=code)[0]

    def update_country(self):
        self.country = self.get_country_object()
        self.save()


class Request(Model):
    """
    Model to register request data
    Check this repo for inspiration:
    https://github.com/django-request/django-request/blob/master/request/models.py

    """

    client = ForeignKey(Client, null=True, on_delete=models.SET_NULL)
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
