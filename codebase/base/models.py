from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models


class Website(Site):
    """
    Website model. Extended version of the Django Site model.

    https://stackoverflow.com/questions/2821702/how-do-you-extend-the-site-model-in-django

    https://docs.djangoproject.com/en/5.1/topics/db/models/#multi-table-inheritance

    """

    title = models.TextField(default="")

    emoji = models.CharField(max_length=8, default="🍊")

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
        return f"{schema}://{self.domain}"

    def __str__(self):
        return self.name
