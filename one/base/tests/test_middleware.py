from http import HTTPStatus

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.http import HttpResponse
from django.test import RequestFactory
from django.urls import reverse

from one.sites.models import Site
from one.test import SimpleTestCase, TestCase
from one.users.factories import SuperuserFactory, UserFactory
from one.users.models import User

from ..middleware.ip import IpAddressMiddleware
from ..middleware.one import OneMiddleware


class TestIpAddressMiddleware(SimpleTestCase):
    request_factory = RequestFactory()
    middleware = IpAddressMiddleware(get_response=lambda request: HttpResponse("Hello"))

    def test_ip_address_no_blocked(self):
        request = self.request_factory.get("/")
        response = self.middleware(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ip_address_blocked(self):
        blocked_ips = {"133.194.187.245", "b40e:95bf:f37:afa0:f325:4c4a:67d7:2cdf"}
        cache.set("blocked_ips", blocked_ips)
        for ip_address in blocked_ips:
            request = self.request_factory.get("/", headers={"X-Real-Ip": ip_address})
            response = self.middleware(request)
            self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestOneMiddleware(TestCase):
    request_factory = RequestFactory()
    middleware = OneMiddleware(get_response=lambda request: HttpResponse("Hello World"))
    ip = "133.194.187.245"

    def get_response(self, ip_address, path="/"):
        site = Site.objects.first()
        request = self.request_factory.get(path, HTTP_HOST=site.domain)
        request.ip_address = ip_address
        request.user = UserFactory()
        return self.middleware(request)

    def test_one_middleware(self):
        response = self.get_response(ip_address=self.ip)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_one_middleware_no_ip(self):
        response = self.get_response(ip_address=None)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_one_middleware_clear_cache(self):
        for clear in (True, False):
            with self.settings(CLEAR_CACHE_IN_DEV=clear):
                response = self.get_response(ip_address=self.ip)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def get_response_from_set_language(
        self,
        user: AnonymousUser | User,
        lang: str = settings.LANGUAGE_CODE,
        langs: None | list = None,
    ):
        site = Site.objects.first()
        if langs:
            site.languages = langs
            site.save()

        url = reverse("set_language")
        request = self.request_factory.post(
            url, HTTP_HOST=site.domain, data={"language": lang}
        )
        request.ip_address = self.ip
        request.user = user
        return self.middleware(request)

    def test_process_language_user_is_authenticated(self):
        lang = "en"
        user = UserFactory()
        response = self.get_response_from_set_language(user=user, lang=lang)

        user.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(user.language, lang)

    def test_process_language_user_is_not_authenticated(self):
        lang = "es"
        response = self.get_response_from_set_language(user=AnonymousUser(), lang=lang)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_process_language_with_multiple_site_langs(self):
        lang = "es"
        response = self.get_response_from_set_language(
            user=AnonymousUser(),
            lang=lang,
            langs=["de", "es"],
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_save_request_skip_saving(self):
        site = Site.objects.first()
        request = self.request_factory.get("/", HTTP_HOST=site.domain)
        request.ip_address = self.ip
        request.user = SuperuserFactory()
        response = self.middleware(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)
