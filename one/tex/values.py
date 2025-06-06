from django.db import models
from django.utils.translation import gettext_lazy as _

TEX_LANGUAGE_MAPPING = {
    # key: django lan
    "en": "english",
    "de": "german",
    "es": "spanish",
    "fr": "french",
    "it": "italian",
    "pt": "portuguese",
    "nl": "dutch",
    "el": "greek",
    "pl": "polish",
    "ru": "russian",
    "sk": "slovak",
    "sl": "slovene",
    "sv": "swedish",
    "tr": "turkish",
    "uk": "ukrainian",
}


class Papersizes(models.TextChoices):
    A3 = "a3paper", "A3 (297 mm x 420 mm)"
    A4 = "a4paper", "A4 (210 mm x 297 mm)"
    A5 = "a5paper", "A5 (148 mm x 210 mm)"
    ANSI_B = "ansibpaper", "ANSI B (11 in. x 17 in.)"
    LETTER = "letterpaper", "ANSI A (8.5 in. x 11 in.)"
    LEGAL_PAPER = "legalpaper", "Legal (8.5 in. x 14 in.)"


class PageOrientations(models.TextChoices):
    PORTRAIT = "portrait", _("Portrait")
    LANDSCAPE = "landscape", _("Landscape")


class PaperUnits(models.TextChoices):
    MILIMITERS = "mm", _("Millimeters")
    INCHES = "in", _("Inches")
