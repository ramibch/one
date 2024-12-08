from django.apps import AppConfig
from django.db.models.signals import post_migrate

from .management import create_languages_in_db


class BaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "codebase.base"

    def ready(self):
        post_migrate.connect(create_languages_in_db, sender=self)
