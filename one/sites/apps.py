from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _

from .management import create_sites_and_necessary_objects


class SitesConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "one.sites"
    verbose_name = _("Sites")

    def ready(self):
        post_migrate.connect(create_sites_and_necessary_objects, sender=self)
