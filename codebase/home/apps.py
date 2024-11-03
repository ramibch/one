from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "codebase.home"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
