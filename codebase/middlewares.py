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

    def __call__(self, request: HttpRequest):
        # Assign coutry to request object
        request.country = CountryDetails(request)  # type: ignore

        # Assign extended site to request
        request.extendedsite = get_current_site(request).extendedsite  # type: ignore

        # Clear cache in development
        self.clear_cache_if_dev()

        # Get response (view process)
        response = self.get_response(request)

        self.check_language(request, response)

        # Process traffic data
        self.process_traffic(request, response)
        return response

    def check_language(self, request, response):
        """
        If the site has just one language, set that one
        """
        if request.extendedsite.languages_count == 1:
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME,
                request.extendedsite.language,
            )

    def clear_cache_if_dev(self):
        """This is better than restarting the http server"""
        if (
            settings.CLEAR_CACHE_IN_DEVELOPMENT
            and settings.DEBUG
            and "django_extensions" in settings.INSTALLED_APPS
        ):
            call_command("clear_cache")

    def process_traffic(self, request, response) -> None:
        """Ignore traffic from staff and for certain urls."""
        exempt_paths = [
            reverse("django_browser_reload:events"),
            reverse("admin:index"),
            reverse("favicon"),
        ]
        path_ok = not any(request.path.startswith(exempt) for exempt in exempt_paths)
        user_ok = not request.user.is_staff
        if path_ok and user_ok:
            TrafficProcessor.process(request, response)


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
        obj = Traffic.objects.create_from_request_and_response(request, response)
        if status_code >= 400:
            # There is an HTTP Error -> inform admin
            url = request.extendedsite.get_object_full_admin_url(obj)  # type: ignore
            Bot.to_admin(f"🔴 {status_code} HTTP Error\n\nCheck traffic object: {url}")
