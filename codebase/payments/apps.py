from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "codebase.payments"
    verbose_name = "00 Payments"

    def ready(self):
        from . import signals  # noqa: F401
