import json

from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from one.base.utils.telegram import Bot

from ..models import UserListing, UserListingFile, UserListingImage, UserShop, UserShopAuth
from .serializers import (AppSerializer, ListingFileSerializer, ListingImageSerializer, ListingSerializer, ShopAuthSerializer,
                          ShopSerializer)


class AuthMixin:
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


class TokenRefreshView(AuthMixin, RetrieveAPIView):
    serializer_class = ShopAuthSerializer

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


class UserListingDetailView(AuthMixin, RetrieveUpdateAPIView):
    serializer_class = ListingSerializer

    def get_queryset(self):
        return UserListing.objects.filter(user_shop_auth=self.user_shop_auth)


class ShopCreateView(AuthMixin, CreateAPIView):
    serializer_class = ShopSerializer

    def perform_create(self, serializer):
        return serializer.save(user_shop_auth=self.user_shop_auth)


class ShopDetailView(AuthMixin, RetrieveUpdateAPIView):
    serializer_class = ShopSerializer

    def get_queryset(self):
        return UserShop.objects.filter(user_shop_auth=self.user_shop_auth)


class ListingCreateView(AuthMixin, CreateAPIView):
    serializer_class = ListingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'user_shop_auth': self.user_shop_auth})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CreateAPIListingFileView(AuthMixin, CreateAPIView):
    """ Base View for Listing Files """
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        listing_id = request.headers.get("x-one-listing-id")
        context = {'listing_id': listing_id, "user_shop_auth": self.user_shop_auth} 
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListingFileCreateView(CreateAPIListingFileView):
    """ Upload a listing file """
    serializer_class = ListingFileSerializer


class ListingImageCreateView(CreateAPIListingFileView):
    """ Upload a listing image """
    serializer_class = ListingImageSerializer



class ListingFileDetailView(AuthMixin, RetrieveUpdateAPIView):
    serializer_class = ListingFileSerializer

    def get_queryset(self):
        return UserListingFile.objects.filter(listing__user_shop_auth=self.user_shop_auth)


class ListingImageDetailView(AuthMixin, RetrieveUpdateAPIView):
    serializer_class = ListingImageSerializer

    def get_queryset(self):
        return UserListingImage.objects.filter(listing__user_shop_auth=self.user_shop_auth)
