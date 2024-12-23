from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.geoip2 import GeoIP2
from django.core.management import call_command
from django.http import HttpRequest
from django.urls import reverse
from django.utils.functional import cached_property

from ...sites.models import Site
from ..models import Traffic
from .telegram import Bot

User = get_user_model()


class Middlewares:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        try:
            x_forwarded_for = request.headers.get("X-Forwarded-For")
            x_real_ip = request.headers.get("X-Real-Ip")
            ip = (
                x_real_ip
                if x_real_ip
                else x_forwarded_for.split(",")[0]
                if x_forwarded_for
                else request.META.get("REMOTE_ADDR")
            )
        except Exception as e:
            Bot.to_admin(f"IP exception: {e}")
            ip = None

        # Assign coutry to request object
        request.country = CountryDetails(ip)  # type: ignore

        # Assign site attribute to request object
        request.site = Site.objects.get(host__name=request.get_host())

        # Clear cache in development
        if settings.DEBUG and settings.ENV == "dev" and settings.CLEAR_CACHE_IN_DEV:
            call_command("clear_cache")

        # Get response (view process)
        response = self.get_response(request)

        # Check and set language
        self.check_and_set_language(request, response)

        # Process traffic data
        self.process_traffic(request, response, ip)

        return response

    def check_and_set_language(self, request, response):
        lang = None

        if request.user.is_authenticated:
            # If the request has user, set the user language
            if request.path == reverse("set_language") and request.method == "POST":
                # User is changing the language
                lang = request.POST.get("language")
                User.objects.filter(id=request.user.id).update(language=lang)
            else:
                lang = request.user.language

        elif request.site.language_count == 1:
            # If the site has just one language, set that one
            lang = request.site.default_language

        if lang is not None:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)

    def process_traffic(self, request, response, ip) -> None:
        """Ignore traffic from staff and for certain urls."""
        exempt_paths = [
            reverse("django_browser_reload:events"),
            reverse("admin:index"),
            reverse("favicon"),
        ]

        path_ok = not any(request.path.startswith(exempt) for exempt in exempt_paths)
        user_ok = not request.user.is_staff

        if path_ok and user_ok:
            status_code = response.status_code
            try:
                obj = Traffic.objects.create_from_request_reponse_and_ip(
                    request=request,
                    response=response,
                    ip=ip,
                )
            except Exception as e:
                Bot.to_admin(f"Traffic saving exception: {e}")
                return

            if status_code >= 400:
                # There is an HTTP Error -> inform admin
                url = request.site.get_object_full_admin_url(obj)  # type: ignore
                Bot.to_admin(
                    f"🔴 {status_code} HTTP Error\n\nCheck traffic object: {url}"
                )


class CountryDetails:
    def __init__(self, ip) -> None:
        self.ip = ip

    @cached_property
    def country_dict(self):
        try:
            return GeoIP2().country(self.ip)
        except Exception as e:
            Bot.to_admin(f"Country exception: {e}")
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
