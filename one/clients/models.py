import operator
from functools import reduce

from auto_prefetch import ForeignKey
from django.contrib.auth import get_user_model
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.geos import Point
from django.db import models
from django.db.models import Case, Q, Value, When
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from one.choices import Countries
from one.db import OneModel

from ..bot import Bot
from ..geo.models import GeoInfo
from ..sites.models import Site

User = get_user_model()


class Path(OneModel):
    name = models.CharField(max_length=512, unique=True, db_index=True)
    is_spam = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Client(OneModel):
    DUMMY_IP_ADDRESS = "10.10.10.10"
    BOTS = [
        "bot",
        "Bot",
        "Python",
        "AppEngine",
        "Mastodon",
        "Crawl",
        "crawl",
        "facebookexternalhit",
        "SnoopSecInspect",
        "letsencrypt.org",
        ".NET",
        "sindresorhus/got",
        "YaSearchApp",
        "Palo Alto Networks",
        "ipip.net",
        "Java",
        "HttpClient",
        "spider",
        "project-resonance.com",
        "Scanner",
        "scanner",
        "Inspect",
        "inspect",
        "Grammarly",
        "GoogleOther",
    ]
    user = ForeignKey(User, null=True, on_delete=models.SET_NULL)
    geoinfo = ForeignKey(
        "geo.GeoInfo",
        null=True,
        on_delete=models.SET_NULL,
        db_index=False,  # Set in meta
    )
    country = models.CharField(max_length=2, choices=Countries, null=True)
    ip_address = models.GenericIPAddressField(unique=True, db_index=True)
    is_blocked = models.BooleanField(default=False)
    user_agent = models.CharField(max_length=512, null=True)
    is_bot = models.GeneratedField(
        expression=Case(
            When(
                reduce(operator.or_, (Q(user_agent__contains=item) for item in BOTS)),
                then=Value(True),
            ),
            default=Value(False),
        ),
        output_field=models.BooleanField(db_default=False),
        db_persist=True,
    )

    class Meta(OneModel.Meta):
        indexes = [
            models.Index(
                name="client_geoinfo_fkey",
                fields=["geoinfo"],
                condition=models.Q(geoinfo__isnull=False),
            )
        ]

    def __str__(self):
        return f"{self.emoji}{'🚫' if self.is_blocked else ''} {self.ip_address}"

    @cached_property
    def emoji(self):
        return "🤖" if self.is_bot else "👤"

    @classmethod
    def dummy_object(cls):
        return cls.objects.get_or_create(ip_address=cls.DUMMY_IP_ADDRESS)[0]

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

    def update_geo_values(self):
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
                params = self.city_data | {"location": Point(lon, lat)}
                self.geoinfo = GeoInfo.objects.create(**params)

        self.save()


class Request(OneModel):
    """
    Model to register request data
    Check this repo for inspiration:
    https://github.com/django-request/django-request/blob/master/request/models.py

    """

    client = ForeignKey(Client, on_delete=models.CASCADE)
    path = ForeignKey(Path, on_delete=models.CASCADE)
    site = ForeignKey(Site, on_delete=models.CASCADE)
    method = models.CharField(default="GET", max_length=7)
    ref = models.CharField(max_length=512, null=True)
    headers = models.TextField(null=True)
    post = models.TextField(null=True)
    status_code = models.PositiveSmallIntegerField(default=200)
    time = models.DateTimeField(_("time"), default=timezone.now)

    def __str__(self):
        time = self.time.strftime("%Y-%m-%d %H:%M")
        return f"[{time}] {self.method} {self.path} {self.status_code}"


class PathRedirect(OneModel):
    sites = models.ManyToManyField("sites.Site")
    from_path = ForeignKey(Path, on_delete=models.CASCADE, related_name="+")
    to_path = ForeignKey(Path, on_delete=models.CASCADE, related_name="+")

    def __str__(self):
        return f"{self.from_path} ➡️ {self.to_path}"
