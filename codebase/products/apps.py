from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "codebase.products"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
