from auto_prefetch import ForeignKey, Manager, Model
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import get_language_info
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class LanguageManager(Manager):
    def sync_languages(self):
        langs = [Language(id=lang) for lang in settings.LANGUAGE_CODES]
        self.bulk_create(
            langs,
            unique_fields=["id"],
            update_fields=["id"],
            ignore_conflicts=True,
        )


class Language(Model):
    id = models.CharField(max_length=8, db_index=True, primary_key=True)

    objects: LanguageManager = LanguageManager()

    def __str__(self):
        return f"{self.name} ({self.id})"

    @cached_property
    def language_info(self) -> dict:
        return get_language_info(self.id)

    @cached_property
    def bidi(self) -> bool:
        return self.language_info.get("bidi")  # type: ignore

    @cached_property
    def code(self) -> str:
        return self.language_info.get("code")  # type: ignore

    @cached_property
    def name(self) -> str:
        return self.language_info.get("name")  # type: ignore

    @cached_property
    def name_local(self) -> str:
        return self.language_info.get("name_local", "")  # type: ignore

    @cached_property
    def capitalize_name_local(self) -> str:
        return self.name_local.capitalize()

    @cached_property
    def name_translated(self) -> str:
        return self.language_info.get("name_translated")  # type: ignore


class TrafficManager(Manager["Traffic"]):
    def create_from_request_and_response(self, request, response) -> "Traffic":
        status_code = response.status_code
        return self.create(
            user=request.user if request.user.is_authenticated else None,
            site=request.site,
            request_path=request.path,
            request_method=request.method,
            request_GET=request.GET,
            request_POST=request.POST,
            request_GET_ref=request.GET.get("ref", None),
            request_headers=request.headers,
            request_country_code=request.country.code,
            response_status_code=status_code,
            response_headers=response.headers,
        )


class Traffic(Model):
    """
    Model to register traffic data
    Check this repo for inspiration:
    https://github.com/django-request/django-request/blob/master/request/models.py

    """

    # Request info
    site = ForeignKey("sites.Site", null=True, on_delete=models.SET_NULL)  # type: ignore
    user = ForeignKey(User, null=True, on_delete=models.SET_NULL)  # type: ignore
    request_path = models.CharField(max_length=255)
    request_method = models.CharField(default="GET", max_length=7)
    request_GET = models.TextField(null=True)
    request_POST = models.TextField(null=True)
    request_GET_ref = models.CharField(max_length=255, null=True)
    request_headers = models.TextField(null=True)
    request_country_code = models.CharField(max_length=8, null=True)

    # Response info
    response_status_code = models.PositiveSmallIntegerField(default=200)
    response_headers = models.TextField(null=True)

    # Others
    time = models.DateTimeField(_("time"), default=timezone.now, db_index=True)

    objects: TrafficManager = TrafficManager()

    def __str__(self):
        return (
            f"[{self.time}] {self.request_method} "
            f"{self.request_path} {self.response_status_code}"
        )
