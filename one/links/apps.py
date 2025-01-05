from django.apps import AppConfig
from django.db.models.signals import post_migrate

from .management import create_necessary_links


class LinksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "one.links"

    def ready(self):
        post_migrate.connect(create_necessary_links, sender=self)
