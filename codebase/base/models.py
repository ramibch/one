from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.functional import cached_property


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

