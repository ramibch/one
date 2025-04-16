from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ClientsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "one.clients"
    verbose_name = _("Clients (HTTP)")
