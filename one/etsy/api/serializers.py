from rest_framework import serializers

from one.base.utils.telegram import Bot

from ..models import App, UserListing, UserListingFile, UserListingImage, UserShop, UserShopAuth


class AppSerializer(serializers.ModelSerializer):
    scopes = serializers.ListField(child=serializers.CharField(), read_only=True)

    class Meta:
        model = App
        fields = ("id", "name", "keystring", "scopes")


class ShopAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserShopAuth
        fields = ("id", "access_token", "refresh_token", "expires_at")



class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserShop
        fields = ("id", "name")


class ListingSerializer(serializers.ModelSerializer):
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
            # "is_personalizable",
            # "personalization_is_required",
            # "personalization_char_count_max",
            # "personalization_instructions",
            # "is_customizable",
            # "should_auto_renew",
            # "is_taxable",
            "listing_type",
        )


    def create(self, validated_data):
        extra =  {"user_shop_auth": self.context.get("user_shop_auth")}
        more_validated_data =validated_data | extra
        return super().create(more_validated_data)



class ListingFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserListingFile
        fields = (
            "listing_file_id",
            "file",
            "name",
            "rank",
        )


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserListingImage
        fields = (
            "image",
            "listing_image_id",
            "rank",
            "name",
            "overwrite",
            "is_watermarked",
            "alt_text",
        )
