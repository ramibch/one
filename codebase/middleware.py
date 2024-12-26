import ipaddress

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.http import HttpRequest
from django.urls import reverse

from .base.utils.telegram import Bot
from .clients.models import Client, Request
from .clients.tasks import update_client_task
from .sites.models import Site

User = get_user_model()


class OneMiddleware:
    """Project middleware"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # Assign site attribute to request object
        request.site = Site.objects.get(host__name=request.get_host())

        # Assign client attribute to request object

        request.client = self.get_client(request)

        # Check if client is blocked
        # if request.client.is_blocked:
        #     return HttpResponseForbidden(_("Your IP Address is blocked."))

        # Clear cache in development
        if settings.DEBUG and settings.ENV == "dev" and settings.CLEAR_CACHE_IN_DEV:
            call_command("clear_cache")

        # Get response (view process)
        response = self.get_response(request)

        # Check and set language
        self.process_language(request, response)

        # Save request object
        self.save_request(request, response)

        return response

    def get_ip_address_or_none(self, request) -> str | None:
        x_forwarded_for_ips = request.headers.get("X-Forwarded-For", "").split(", ")
        x_real_ip = request.headers.get("X-Real-Ip", "")
        remote_addr = request.META.get("REMOTE_ADDR", "")

        raw_addresses = (x_real_ip, *x_forwarded_for_ips, remote_addr)
        exempt_addresses = (None, "", "127.0.0.1", "localhost")
        addresses = {addr for addr in raw_addresses if addr not in exempt_addresses}
        ips = {ipaddress.ip_address(addr) for addr in addresses}

        ipsv4 = [str(ip) for ip in ips if ip.version == 4]
        ipsv6 = [str(ip) for ip in ips if ip.version == 6]

        if ipsv4:
            return ipsv4[0]
        if ipsv6:
            return ipsv6[0]

        if settings.ENV == "prod":
            Bot.to_admin(f"No IPv4 or IPv6 Addresses found for {request}\n{ips}")

    def get_user_agent(self, request):
        http_user_agent = request.META.get("HTTP_USER_AGENT", "")[:256]
        if http_user_agent != "":
            return http_user_agent
        else:
            return request.headers.get("User-Agent", "")[:256]

    def get_client(self, request) -> Client:
        ip = self.get_ip_address_or_none(request)

        if ip is None:
            return Client.dummy_object()

        user_or_none = request.user if request.user.is_authenticated else None

        try:
            client = Client.objects.get(ip_address=ip)
        except Client.DoesNotExist:
            client = Client.objects.create(
                ip_address=ip,
                user=user_or_none,
                site=request.site,
                is_blocked=False,
                user_agent=self.get_user_agent(request),
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
                User.objects.filter(id=request.user.id).update(language=lang)
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
            except Exception as e:
                Bot.to_admin(f"Error by saving request obj: {e}")
