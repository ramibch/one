from rest_framework import serializers

from one.base.utils.telegram import Bot
from one.books.models import User

from ..models import App, EtsyAuth, Listing, ListingFile, Shop, UserListingImage


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
        fields = ("id", "name")


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
            "listing_type"
        )


    def create(self, validated_data):
        extra =  {"user_shop_auth": self.context.get("user_shop_auth")}
        more_validated_data =validated_data | extra
        return super().create(more_validated_data)


class ListingFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingFile
        fields = ("file",)
    
    def create(self, validated_data):
        user_shop_auth = self.context.get("user_shop_auth")
        listing_id = self.context.get("listing_id")
        listing = Listing.objects.get(id=listing_id, user_shop_auth=user_shop_auth)
        last_file = listing.userlistingfile_set.last()
        rank = 1 if last_file is None else last_file.rank + 1
        extra =  {"listing": listing, "rank": rank}
        more_validated_data =validated_data | extra
        return super().create(more_validated_data)


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserListingImage
        fields = ("file",)

    def create(self, validated_data):
        user_shop_auth = self.context.get("user_shop_auth")
        listing_id = self.context.get("listing_id")
        listing = Listing.objects.get(id=listing_id, user_shop_auth=user_shop_auth)
        last_file = listing.userlistingimage_set.last()
        rank = 1 if last_file is None else last_file.rank + 1
        extra =  {"listing": listing, "rank": rank}
        more_validated_data =validated_data | extra
        return super().create(more_validated_data)
