from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpRequest
from django.utils.functional import cached_property


class CountryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.country = CountryDetails(request)
        return self.get_response(request)


class CountryDetails:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request

    def _get_country_dict(self):
        # get IP
        x_forwarded_for = self.request.headers.get("x-forwarded-for")
        ip = x_forwarded_for.split(",")[0] if x_forwarded_for else self.request.META.get("REMOTE_ADDR")

        try:
            country_dict = GeoIP2().country(ip)
        except Exception:
            country_dict = {"country_code": None, "country_name": None}

        return country_dict

    @cached_property
    def code(self) -> str:
        return self._get_country_dict()["country_code"]

    @cached_property
    def name(self) -> str:
        return self._get_country_dict()["country_name"]

    def __str__(self):
        return self.code
