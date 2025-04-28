from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.core.management import call_command
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from one.clients.tasks import save_request_task

from ...clients.models import Client, PathRedirect
from ...sites.models import Site


class OneMiddleware:
    """Project middleware"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # Assign site attribute to request object
        request.site = Site.objects.get_current(request=request)

        # Check redirect
        redirect_obj = self.get_redirect_or_none(request)
        if redirect_obj:
            return HttpResponseRedirect(redirect_obj.to_path.name)

        # Assign client attribute to request object
        request.client = self.get_client(request)

        # Assign session
        request.db_session = self.get_session(request)

        # Valid Project api secret
        # Use for API POST calls without user authentication
        request.has_valid_one_secret_key = self.valid_secret_key(request)

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

    def valid_secret_key(self, request):
        return request.headers.get("x-one-secret-key") == settings.ONE_SECRET_KEY

    def get_session(self, request):
        try:
            session_key = request.session.session_key
            db_session = Session.objects.get(pk=session_key)
        except (KeyError, Session.DoesNotExist):
            session_store = SessionStore()
            session_store.create()
            session_key = session_store.session_key
            request.session["sessionid"] = session_key
            db_session = Session.objects.get(session_key=session_key)
        return db_session

    def get_redirect_or_none(self, request):
        return PathRedirect.objects.filter(
            sites=request.site, from_path__name=request.path
        ).first()

    def get_user_agent(self, request):
        return request.headers.get("user-agent", "")[:256]

    def get_client(self, request) -> Client:
        if request.ip_address == Client.DUMMY_IP_ADDRESS:
            return Client.dummy_object()

        try:
            client = Client.objects.get(ip_address=request.ip_address)
        except Client.DoesNotExist:
            client = Client.objects.create(
                ip_address=request.ip_address,
                user=request.user if request.user.is_authenticated else None,
                is_blocked=False,
                user_agent=self.get_user_agent(request),
            )

            client.update_geo_values()

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
            lang = request.site.language

        if lang is not None:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)

    def save_request(self, request, response):
        skip_paths = [
            reverse_lazy("admin:index"),
            reverse_lazy("favicon"),
        ]
        client = self.get_client(request)

        path_ok = not any(request.path.startswith(str(p)) for p in skip_paths)
        user_ok = not request.user.is_staff
        status_ok = response.status_code >= 400 and client.is_bot or not client.is_bot

        if path_ok and user_ok and status_ok:
            params = {
                "client": client,
                "path_name": request.path[:255],
                "method": request.method,
                "ref": request.GET.get("ref", "")[:256],
                "headers": request.headers,
                "site": request.site,
                "status_code": response.status_code,
                "post": str(request.POST),
            }
            save_request_task(params)
