from rest_framework.serializers import ModelSerializer

from .models import UserListing, UserShopAuth


class UserShopAuthSerializer(ModelSerializer):
    class Meta:
        model = UserShopAuth
        fields = ("id", "access_token", "refresh_token", "expires_at")


class UserListingSerializer(ModelSerializer):
    class Meta:
        model = UserListing
        fields = (
            "quantity",
            "title",
            "description",
            "price",
            "who_made",
            "when_made",
            "taxonomy_id",
            "shop_section_id",
            "tags",
            "is_personalizable",
            "personalization_is_required",
            "personalization_char_count_max",
            "personalization_instructions",
            "is_customizable",
            "should_auto_renew",
            "is_taxable",
            "listing_type",
        )
