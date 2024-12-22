from django.db import models
from django.utils.translation import gettext_lazy as _


class Language(models.TextChoices):
    EN = "en", _("English")
    DE = "de", _("German")
    ES = "es", _("Spanish")
    FR = "fr", _("French")
    EL = "el", _("Greek")
    IT = "it", _("Italian")
    NL = "nl", _("Dutch")
    PL = "pl", _("Polish")
    PT = "pt", _("Portuguese")
    RU = "ru", _("Russian")
    SK = "sk", _("Slovak")
    SL = "sl", _("Slovenian")
    SV = "sv", _("Swedish")
    TR = "tr", _("Turkish")
    OK = "uk", _("Ukrainian")
