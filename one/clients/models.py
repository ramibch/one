from auto_prefetch import ForeignKey, Model
from django.contrib.auth import get_user_model
from django.contrib.gis.geoip2 import GeoIP2
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from ..base import Countries
from ..base.utils.telegram import Bot
from ..geo.models import GeoInfo
from ..sites.models import Site

User = get_user_model()


class Path(Model):
    name = models.CharField(max_length=512, unique=True, db_index=True)
    is_spam = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Client(Model):
    DUMMY_IP_ADDRESS = "10.10.10.10"
    user = ForeignKey(User, null=True, on_delete=models.SET_NULL)
    country = models.CharField(max_length=2, choices=Countries, default="CH")
    site = ForeignKey("sites.Site", null=True, on_delete=models.SET_NULL)
    geoinfo = ForeignKey("geo.GeoInfo", null=True, on_delete=models.SET_NULL)
    ip_address = models.GenericIPAddressField(unique=True, db_index=True)
    is_blocked = models.BooleanField(default=False)
    user_agent = models.CharField(max_length=512, null=True)
    dark_theme = models.BooleanField(default=True)

    def __str__(self):
        return self.ip_address

    @classmethod
    def dummy_object(cls):
        try:
            return cls.objects.get(ip_address=cls.DUMMY_IP_ADDRESS)
        except cls.DoesNotExist:
            obj = cls(
                ip_address=cls.DUMMY_IP_ADDRESS,
                site=Site.development.first(),
            )
            obj.save()
            return obj

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
        lat, lon = self.city_data.get("latitude"), self.city_data.get("longitude")
        if all((lat, lon)):
            geoinfo = GeoInfo.objects.filter(latitude=lat, longitude=lon).first()
            if geoinfo:
                self.geoinfo = geoinfo
            else:
                self.geoinfo = GeoInfo.objects.create(**self.city_data)

        self.save()


class Request(Model):
    """
    Model to register request data
    Check this repo for inspiration:
    https://github.com/django-request/django-request/blob/master/request/models.py

    """

    client = ForeignKey(Client, on_delete=models.CASCADE)
    path = ForeignKey(Path, on_delete=models.CASCADE, null=True)
    method = models.CharField(default="GET", max_length=7)
    get = models.TextField(null=True)
    post = models.TextField(null=True)
    ref = models.CharField(max_length=512, null=True, db_index=True)
    headers = models.TextField(null=True)
    status_code = models.PositiveSmallIntegerField(default=200)
    time = models.DateTimeField(_("time"), default=timezone.now, db_index=True)

    def save_from_midddleware(self, request, response):
        self.client = request.client
        self.path = Path.objects.get_or_create(name=request.path[:255])[0]
        self.method = request.method
        self.get = request.GET
        self.post = request.POST
        self.ref = request.GET.get("ref", "")[:256]
        self.headers = request.headers
        self.status_code = response.status_code
        self.save()

    def __str__(self):
        time = self.time.strftime("%Y-%m-%d %H:%M")
        return f"[{time}] {self.method} {self.path} {self.status_code}"


class RedirectTypes(models.TextChoices):
    USER = "user", "👤 " + _("For logged users")
    NO_USER = "no_user", "🕵🏻 " + _("For anonymous users")
    ALWAYS = "always", "🔄 " + _("Always")


class PathRedirect(Model):
    site = ForeignKey("sites.Site", on_delete=models.CASCADE)
    from_path = ForeignKey(Path, on_delete=models.CASCADE, related_name="+")
    to_path = ForeignKey(Path, on_delete=models.CASCADE, related_name="+")
    applicable = models.CharField(
        default=RedirectTypes.ALWAYS,
        choices=RedirectTypes.choices,
        max_length=16,
    )

    def __str__(self):
        return f"[{self.site}] {self.from_path} ➡️ {self.to_path}"
