from django.apps import AppConfig


class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "one.search"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
