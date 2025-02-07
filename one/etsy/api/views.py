# from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView

from one.base.utils.telegram import Bot

from ..models import UserListing, UserListingFile, UserListingImage, UserShopAuth
from ..serializers import (AppSerializer, UserListingFileSerializer, UserListingImageSerializer, UserListingSerializer,
                           UserShopAuthSerializer, UserShopSerializer)


class UserShopAuthMixin:
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        shop_id = request.META.get("HTTP_X_ETSY_SHOP_ID")
        user_id = request.META.get("HTTP_X_ETSY_USER_ID")
        code = request.META.get("HTTP_X_ETSY_CODE")
        if None in (shop_id, user_id, code):
            msg = "Missing: x-etsy-shop-id, x-etsy-user-id or x-etsy-code"
            raise PermissionDenied(msg)

        # User auth object
        try:
            self.user_shop_auth = UserShopAuth.objects.get(
                shop_id=shop_id,
                etsy_user_id=user_id,
                code=code,
            )
        except UserShopAuth.DoesNotExist as err:
            adm_msg = f"⚠️ {UserShopAuth.__name__} no object match\n"
            adm_msg += f"shop_id = {shop_id}\n"
            adm_msg += f"user_id = {user_id}\n"
            adm_msg += f"cod e= {code}"
            Bot.to_admin(adm_msg)
            msg = _("No authorization, contact admin/seller.")
            raise PermissionDenied(msg) from err
        except UserShopAuth.MultipleObjectsReturned:
            self.user_shop_auth = (
                UserShopAuth.objects.filter(
                    shop_id=shop_id,
                    etsy_user_id=user_id,
                    code=code,
                )
                .order_by("-expires_at")
                .filter()
            )
        
        return super().dispatch(request, *args, **kwargs)


class TokenRefreshView(UserShopAuthMixin, RetrieveAPIView):
    serializer_class = UserShopAuthSerializer

    def get_object(self):
        obj = self.user_shop_auth
        ref_time = timezone.now() - timezone.timedelta(minutes=10)
        if ref_time > obj.expires_at:
            obj.get_api_client().refresh()
            obj.refresh_from_db()
        return obj


class AppCreateView(CreateAPIView):
    serializer_class = AppSerializer

    def post(self, request, *args, **kwargs):
        if request.has_valid_one_secret_key:
            return super().post(request, *args, **kwargs)
        else:
            raise PermissionDenied


class UserListingDetailView(UserShopAuthMixin, RetrieveUpdateAPIView):
    serializer_class = UserListingSerializer

    def get_queryset(self):
        return UserListing.objects.filter(user_shop_auth=self.user_shop_auth)


class UserShopCreateView(UserShopAuthMixin, CreateAPIView):
    serializer_class = UserShopSerializer

    def perform_create(self, serializer):
        return serializer.save(user_shop_auth=self.user_shop_auth)
    

class UserListingCreateView(UserShopAuthMixin, CreateAPIView):
    serializer_class = UserListingSerializer
    permission_classes = (permissions.AllowAny,)


class UserListingFileCreateView(UserShopAuthMixin, CreateAPIView):
    serializer_class = UserListingFileSerializer


class UserListingFileDetailView(UserShopAuthMixin, RetrieveUpdateAPIView):
    serializer_class = UserListingFileSerializer

    def get_queryset(self):
        return UserListingFile.objects.filter(listing__user_shop_auth=self.user_shop_auth)


class UserListingImageCreateView(UserShopAuthMixin, CreateAPIView):
    serializer_class = UserListingImageSerializer


class UserListingImageDetailView(UserShopAuthMixin, RetrieveUpdateAPIView):
    serializer_class = UserListingImageSerializer

    def get_queryset(self):
        return UserListingImage.objects.filter(listing__user_shop_auth=self.user_shop_auth)
