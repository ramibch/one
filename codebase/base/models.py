from auto_prefetch import ForeignKey, Model
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class ExtendedSite(Site):
    remarks = models.TextField(null=True, blank=True)

    emoji = models.CharField(max_length=8, null=True)
    emoji_in_brand = models.BooleanField(default=True)
    default_page_title = models.CharField(max_length=64, null=True)
    default_page_description = models.TextField(max_length=256, null=True)
    default_page_keywords = models.TextField(max_length=128, null=True)

    change_theme_light_in_footer = models.BooleanField(default=True)
    change_theme_light_in_navbar = models.BooleanField(default=True)
    change_language_in_navbar = models.BooleanField(default=True)
    change_language_in_footer = models.BooleanField(default=True)

    # Management
    allow_field_translation = models.BooleanField(default=False)
    last_huey_flush = models.DateTimeField(null=True)
    has_user_home = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @cached_property
    def url(self):
        schema = "https" if settings.HTTPS else "http"
        return f"{schema}://{self.domain}"

    def get_admin_url_for_model_instance(self, obj):
        # the url to the Django admin form for the model instance
        info = (obj._meta.app_label, obj._meta.model_name)
        return reverse("admin:{}_{}_change".format(*info), args=(obj.pk,))

    def get_full_admin_url_for_model_instance(self, obj):
        return self.url + self.get_admin_url_for_model_instance(obj)


class Traffic(Model):
    # Request info
    request_path = models.CharField(max_length=255)
    request_method = models.CharField(default="GET", max_length=7)
    request_GET = models.TextField(null=True)
    request_POST = models.TextField(null=True)
    request_GET_ref = models.CharField(max_length=255, null=True)
    request_headers = models.TextField(null=True)
    request_user = ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    request_country_code = models.CharField(max_length=8, null=True)
    request_site = ForeignKey(Site, blank=True, null=True, on_delete=models.SET_NULL)

    # Response info
    response_code = models.PositiveSmallIntegerField(default=200)
    response_headers = models.TextField(null=True)

    # Others
    time = models.DateTimeField(_("time"), default=timezone.now, db_index=True)

    def __str__(self):
        return f"[{self.time}] {self.request_method} {self.request_path} {self.response_code}"
