from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmailsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "one.emails"
    verbose_name = _("Emails")
