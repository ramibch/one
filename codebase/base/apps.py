from django.apps import AppConfig
from django.core.checks import register


class BaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "codebase.base"

    def ready(self):
        from . import checks

        register(checks.check_abstract_models)
