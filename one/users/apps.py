from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "one.users"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
