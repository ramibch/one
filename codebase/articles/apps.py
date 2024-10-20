from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "codebase.articles"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
