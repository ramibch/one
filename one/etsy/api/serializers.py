from rest_framework import serializers

from one.base.utils.telegram import Bot
from one.books.models import User

from ..models import App, EtsyAuth, Listing, ListingFile, ListingImage, Shop


class AppSerializer(serializers.ModelSerializer):
    scopes = serializers.ListField(child=serializers.CharField(), read_only=True)

    class Meta:
        model = App
        fields = ("id", "name", "keystring", "scopes")


class ShopAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtsyAuth
        fields = ("id", "access_token", "refresh_token", "expires_at")



class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = (
            "shop_id",
            "shop_name",
            "user_id",
            "title",
            "announcement",
            "currency_code",
            "listing_active_count",
            "digital_listing_count",
            "url",
            "num_favorers",
            "languages",
            "transaction_sold_count",
            "review_average",
            "review_count",
            )


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = (
            "id",
            "quantity",
            "title",
            "description",
            "price",
            "who_made",
            "when_made",
            "taxonomy_id",
            "shop_section_id",
            "tags",
            "listing_type",
            "is_personalizable",
            "listing_id",
            "url",
        )
        read_only_fields = ("url", "listing_id")


    def create(self, validated_data):
        extra =  {"etsy_auth": self.context.get("etsy_auth")}
        more_validated_data =validated_data | extra
        return super().create(more_validated_data)


class ListingFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingFile
        fields = ("file",)
    
    def create(self, validated_data):
        etsy_auth = self.context.get("etsy_auth")
        listing_id = self.context.get("listing_id")
        listing = Listing.objects.get(id=listing_id, etsy_auth=etsy_auth)
        last_file = listing.files.last()
        rank = 1 if last_file is None else last_file.rank + 1
        extra =  {"listing": listing, "rank": rank}
        more_validated_data =validated_data | extra
        return super().create(more_validated_data)


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ("file",)

    def create(self, validated_data):
        etsy_auth = self.context.get("etsy_auth")
        listing_id = self.context.get("listing_id")
        listing = Listing.objects.get(id=listing_id, etsy_auth=etsy_auth)
        last_file = listing.images.last()
        rank = 1 if last_file is None else last_file.rank + 1
        extra =  {"listing": listing, "rank": rank}
        more_validated_data =validated_data | extra
        return super().create(more_validated_data)

