from django.apps import AppConfig
from django.core.checks import register
from django.db.models.signals import post_migrate

from .management import create_languages_in_db


class BaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "codebase.base"

    def ready(self):
        from . import checks

        post_migrate.connect(create_languages_in_db, sender=self)
        register(checks.check_abstract_models)
