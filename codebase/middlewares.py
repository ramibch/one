from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.sites.shortcuts import get_current_site
from django.core.management import call_command
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.utils.functional import cached_property

from .base.models import Traffic
from .utils.telegram import Bot


class Middlewares:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Assign coutry to request object
        request.country = CountryDetails(request)

        # Clear cache in development
        self.clear_cache_if_dev()

        response = self.get_response(request)

        # Process traffic data
        if self.can_we_process_traffic(request.path, request.user):
            TrafficProcessor.process(request, response)

        return response

    def clear_cache_if_dev(self):
        """This is better than restarting the http server"""
        if (
            settings.CLEAR_CACHE_IN_DEVELOPMENT
            and settings.DEBUG
            and "django_extensions" in settings.INSTALLED_APPS
        ):
            call_command("clear_cache")

    def can_we_process_traffic(self, path: str, user) -> bool:
        """Ignore traffic from staff and for certain urls."""
        exempt_paths = [
            reverse("django_browser_reload:events"),
            reverse("admin:index"),
            reverse("favicon"),
        ]

        path_ok = not any(path.startswith(exempt) for exempt in exempt_paths)
        user_ok = not user.is_staff

        return path_ok and user_ok


class CountryDetails:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request

    @cached_property
    def country_dict(self):
        x_forwarded_for = self.request.headers.get("x-forwarded-for")
        ip = (
            x_forwarded_for.split(",")[0]
            if x_forwarded_for
            else self.request.META.get("REMOTE_ADDR")
        )

        try:
            return GeoIP2().country(ip)
        except Exception:
            return {
                "country_code": None,
                "country_name": None,
                "continent_code": None,
                "continent_name": None,
                "is_in_european_union": None,
            }

    @cached_property
    def code(self) -> str:
        return self.country_dict["country_code"]

    @cached_property
    def name(self) -> str:
        return self.country_dict["country_name"]

    def __str__(self):
        return self.code


class TrafficProcessor:
    @staticmethod
    def process(request: HttpRequest, response: HttpResponse):
        status_code = response.status_code
        obj = Traffic.objects.create_object_from_request_and_response(request, response)
        if status_code >= 400:
            # There is an HTTP Error -> inform admin
            url = get_current_site(request).extendedsite.get_object_full_admin_url(obj)
            Bot.to_admin(f"🔴 {status_code} HTTP Error\n\nCheck traffic object: {url}")
