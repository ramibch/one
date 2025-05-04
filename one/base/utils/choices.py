from django.db import models
from django.utils.translation import gettext_lazy as _


class Genders(models.TextChoices):
    MALE = "m", _("male")
    FEMALE = "f", _("female")
