from auto_prefetch import Model, OneToOneField
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models


class ExtendedSite(Model):
    site = OneToOneField(Site, null=True, on_delete=models.SET_NULL, related_name="extended")

    remarks = models.TextField(null=True, blank=True)

    emoji = models.CharField(max_length=8, default="")

    emoji_in_brand = models.BooleanField(default=True)

    default_page_title = models.CharField(max_length=64)

    default_page_description = models.TextField(max_length=256)

    default_page_keywords = models.CharField(max_length=128)

    change_theme_light_in_footer = models.BooleanField(default=True)

    change_theme_light_in_navbar = models.BooleanField(default=True)

    # Managements attrs
    last_huey_flush = models.DateTimeField(null=True)

    def url(self):
        schema = "https" if settings.HTTPS else "http"
        return f"{schema}://{self.site.domain}"

    def __str__(self):
        return self.site.name

    class Meta(Model.Meta):
        app_label = "sites"
