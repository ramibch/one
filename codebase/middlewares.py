from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.sites.shortcuts import get_current_site
from django.core.management import call_command
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.utils.functional import cached_property
from huey.contrib import djhuey as huey

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
        if settings.CLEAR_CACHE_IN_DEVELOPMENT and settings.DEBUG and "django_extensions" in settings.INSTALLED_APPS:
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
        ip = x_forwarded_for.split(",")[0] if x_forwarded_for else self.request.META.get("REMOTE_ADDR")

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
    def process(request: HttpRequest, response: HttpResponse) -> None:
        request_params = TrafficProcessor.get_request_params(request)
        response_params = TrafficProcessor.get_response_params(response)
        TrafficProcessor.save_traffic_data(request_params, response_params)

    @staticmethod
    def get_request_params(request: HttpRequest):
        return {
            "path": request.path,
            "method": request.method,
            "GET": request.GET,
            "POST": request.POST,
            "headers": request.headers,
            "user": request.user if request.user.is_authenticated else None,
            "site": get_current_site(request),
            "country_code": request.country.code,
        }

    @staticmethod
    def get_response_params(response: HttpResponse):
        return {
            "headers": response.headers,
            "code": response.status_code,
        }

    @staticmethod
    @huey.task()
    def save_traffic_data(request_params: dict, response_params: dict):
        response_code = response_params.get("code")
        request_site = request_params.get("site")

        traffic_obj = Traffic.objects.create(
            request_path=request_params.get("path"),
            request_method=request_params.get("method"),
            request_GET=request_params.get("GET"),
            request_POST=request_params.get("POST"),
            request_GET_ref=request_params.get("GET").get("ref", None),
            request_headers=request_params.get("headers"),
            request_user=request_params.get("user"),
            request_country_code=request_params.get("country_code"),
            request_site=request_site,
            response_code=response_code,
            response_headers=response_params.get("headers"),
        )

        if response_code >= 400:
            # There is an HTTP Error -> inform admin
            obj_admin_url = request_site.extendedsite.get_full_admin_url_for_model_instance(traffic_obj)
            Bot.to_admin(f"🔴 HTTP Status Error {response_code}\n\nCheck traffic object: {obj_admin_url}")
