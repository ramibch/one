from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _

from .management import create_default_sites


class SitesConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "codebase.sites"
    verbose_name = _("Sites")

    def ready(self):
        post_migrate.connect(create_default_sites, sender=self)
