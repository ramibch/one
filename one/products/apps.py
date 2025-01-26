from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "one.products"
    verbose_name = "00 Products"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
