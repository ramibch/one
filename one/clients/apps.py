from django.apps import AppConfig


class ClientsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "one.clients"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
