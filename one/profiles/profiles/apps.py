from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "one.profiles"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
