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


class Scopes(models.TextChoices):
    ADDRESS_READ = "address_r", _("address_r: see billing and shipping addresses")
    ADDRESS_WRITE = "address_w", _("address_w: update billing and shipping addresses")
    BILLING_READ = "billing_r", _("billing_r: see all billing statement data")
    CART_READ = "cart_r", _("cart_r: read shopping carts")
    CART_WRITE = "cart_w", _("cart_w: add/remove from shopping carts")
    EMAIL_READ = "email_r", _("email_r: read a user profile")
    FAVORITES_READ = "favorites_r", _("favorites_r: see private favorites")
    FAVORITES_WRITE = "favorites_w", _("favorites_w: add/remove favorites")
    FEEDBACK_READ = "feedback_r", _("feedback_r: see purchase info in feedback")
    LISTINGS_DELETE = "listings_d", _("listings_d: delete listings")
    LISTINGS_READ = ("listings_r", _("listings_r: see all listings "))
    LISTINGS_WRITE = "listings_w", _("listings_w: create/edit listings")
    PROFILE_READ = "profile_r", _("profile_r: see all profile data")
    PROFILE_WRITE = "profile_w", _("profile_w: update user profile, avatar, etc.")
    RECOMMEND_READ = "recommend_r", _("recommend_r: see recommended listings")
    RECOMMEND_W = ("recommend_w", _("recommend_w: accept/reject recommended listings"))
    SHOPS_READ = "shops_r", _("shops_r: see private shop info")
    SHOPS_WRITE = "shops_w", _("shops_w: update shop")
    TRANSACTIONS_READ = ("transactions_r", _("transactions_r: see all payment data"))
    TRANSACTIONS_WRITE = "transactions_w", _("transactions_w: update receipts")
