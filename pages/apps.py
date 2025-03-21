from django.apps import AppConfig


class PagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "one.pages"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
