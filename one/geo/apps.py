from django.apps import AppConfig


class GeoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "one.geo"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
