from rest_framework import serializers

from .models import App, UserListing, UserListingFile, UserListingImage, UserShopAuth


class AppSerializer(serializers.ModelSerializer):
    scopes = serializers.ListField(child=serializers.CharField(), read_only=True)

    class Meta:
        model = App
        fields = ("id", "name", "keystring", "scopes")


class UserShopAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserShopAuth
        fields = ("id", "access_token", "refresh_token", "expires_at")


class UserListingSerializer(serializers.ModelSerializer):
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


class UserListingFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserListingFile
        fields = (
            "listing_file_id",
            "file",
            "name",
            "rank",
        )


class UserListingImageSerializer(serializers.ModelSerializer):
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
