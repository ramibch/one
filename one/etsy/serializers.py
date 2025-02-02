
from rest_framework import serializers


from .models import UserShopAuth


class UserShopAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserShopAuth
        fields = ('id', 'access_token', 'refresh_token', "expires_at")