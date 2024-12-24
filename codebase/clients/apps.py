from django.apps import AppConfig


class ClientsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "codebase.clients"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa