from django.conf import settings
from django.core.management import call_command
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse

from ...clients.models import Client, PathRedirect, RedirectTypes, Request
from ...clients.tasks import update_client_task
from ...sites.models import Site
from ..utils.telegram import Bot


class OneMiddleware:
    """Project middleware"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # Assign site attribute to request object
        request.site = Site.objects.get(host__name=request.get_host())

        # Check redirect
        redirect_obj = self.get_redirect_or_none(request)
        if redirect_obj:
            return HttpResponseRedirect(redirect_obj.to_path.name)

        # Assign client attribute to request object
        request.client = self.get_client(request)

        # Clear cache in development
        if settings.ENV == "dev" and settings.CLEAR_CACHE_IN_DEV:
            call_command("clear_cache")

        # Get response (view process)
        response = self.get_response(request)

        # Check and set language
        self.process_language(request, response)

        # Save request object
        self.save_request(request, response)

        return response

    def get_redirect_or_none(self, request):
        applicable = [
            RedirectTypes.USER
            if request.user.is_authenticated
            else RedirectTypes.NO_USER,
            RedirectTypes.ALWAYS,
        ]
        return PathRedirect.objects.filter(
            site=request.site,
            from_path__name=request.path,
            applicable__in=applicable,
        ).first()

    def get_client(self, request) -> Client:
        if request.ip_address is None:
            return Client.dummy_object()

        user_or_none = request.user if request.user.is_authenticated else None

        try:
            client = Client.objects.get(ip_address=request.ip_address)
        except Client.DoesNotExist:
            client = Client.objects.create(
                ip_address=request.ip_address,
                user=user_or_none,
                site=request.site,
                is_blocked=False,
                user_agent=request.META.get("HTTP_USER_AGENT", "")[:256],
            )
            update_client_task(client)

        return client

    def process_language(self, request, response):
        lang = None

        if request.user.is_authenticated:
            # If the request has user, set the user language
            if request.path == reverse("set_language") and request.method == "POST":
                # User is changing the language
                lang = request.POST.get("language")
                request.user.language = lang
                request.user.save()
            else:
                lang = request.user.language

        elif request.site.language_count == 1:
            # If the site has just one language, set that one
            lang = request.site.default_language

        if lang is not None:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)

    def save_request(self, request, response):
        exempt_paths = [
            reverse("django_browser_reload:events"),
            reverse("admin:index"),
            reverse("favicon"),
        ]

        path_ok = not any(request.path.startswith(exempt) for exempt in exempt_paths)
        user_ok = not request.user.is_staff

        if path_ok and user_ok:
            try:
                Request().save_from_midddleware(request=request, response=response)
            except Exception as e:  # pragma: no cover
                Bot.to_admin(f"Error by saving request obj: {e}")
