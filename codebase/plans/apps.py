from django.apps import AppConfig


class PlansConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "codebase.plans"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
