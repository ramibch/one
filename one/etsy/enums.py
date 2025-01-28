from django.db import models
from django.utils.translation import gettext_lazy as _


class TaxonomyID(models.IntegerChoices):
    DIGITAL_PRINTS = 2078, _("Digital prints")


class WhenMade(models.TextChoices):
    MADE_TO_ORDER = "made_to_order", _("Made to order")
    YEARS_2020_2025 = "2020_2025", "2020 - 2025"
    YEARS_2010_2019 = "2010_2019", "2010 - 2019"
    YEARS_2006_2009 = "2006_2009", "2006 - 2009"
    BEFORE_2006 = "before_2006", _("Before 2006")


class WhoMade(models.TextChoices):
    I_DID = "i_did", _("I did")
    SOMEONE_ELSE = "someone_else", _("Someone else")
    COLLECTIVE = "collective", _("Collective")


class ListingType(models.TextChoices):
    PHYSICAL = "physical", _("Physical")
    DOWNLOAD = "download", _("Download")
    BOTH = "both", _("Both")
