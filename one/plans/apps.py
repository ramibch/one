from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PlansConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "one.plans"
    verbose_name = _("Plans")
