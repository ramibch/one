from django.apps import AppConfig


class BooksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "one.books"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
