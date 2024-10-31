from django.apps import AppConfig


class MenusConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "codebase.menus"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
