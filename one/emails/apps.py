from django.apps import AppConfig


class EmailsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "one.emails"
    verbose_name = "00 Emails"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
