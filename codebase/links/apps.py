from django.apps import AppConfig


class LinksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "codebase.links"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
