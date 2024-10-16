from __future__ import annotations

from django.apps import AppConfig


class TestappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "code.testapp"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
