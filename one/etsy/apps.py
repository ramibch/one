from django.apps import AppConfig


class EtsyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "one.etsy"
    verbose_name = "00 Etsy"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
