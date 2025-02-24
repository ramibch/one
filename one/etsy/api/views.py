import json
from http import HTTPStatus

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

from ..models import App, EtsyAuth, Listing, ListingFile, ListingImage, Shop
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
            self.etsy_auth = EtsyAuth.objects.get(
                shop_id=shop_id,
                etsy_user_id=user_id,
                code=code,
            )
        except EtsyAuth.DoesNotExist as err:
            adm_msg = f"⚠️ {EtsyAuth.__name__} no object match\n"
            adm_msg += f"shop_id = {shop_id}\n"
            adm_msg += f"user_id = {user_id}\n"
            adm_msg += f"cod e= {code}"
            Bot.to_admin(adm_msg)
            msg = _("No authorization, contact admin/seller.")
            raise PermissionDenied(msg) from err
        except EtsyAuth.MultipleObjectsReturned:
            self.etsy_auth = (
                EtsyAuth.objects.filter(
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
        obj = self.etsy_auth
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

class CommercialAppDetailView(RetrieveAPIView):
    serializer_class = AppSerializer
    queryset = App.objects.filter(is_commercial=True)

    def get_object(self):
        return self.queryset.last()
    
    def get(self, request, *args, **kwargs):
        if self.get_object() and request.has_valid_one_secret_key:
            return super().get(self, request, *args, **kwargs)
        return Response(status=HTTPStatus.NOT_FOUND)


class UserListingDetailView(AuthMixin, RetrieveUpdateAPIView):
    serializer_class = ListingSerializer

    def get_queryset(self):
        return Listing.objects.filter(etsy_auth=self.etsy_auth)


class ShopCreateView(AuthMixin, CreateAPIView):
    serializer_class = ShopSerializer

    def perform_create(self, serializer):
        return serializer.save(etsy_auth=self.etsy_auth)


class ShopDetailView(AuthMixin, RetrieveUpdateAPIView):
    serializer_class = ShopSerializer

    def get_queryset(self):
        return Shop.objects.filter(etsy_auth=self.etsy_auth)


class ListingCreateView(AuthMixin, CreateAPIView):
    serializer_class = ListingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'etsy_auth': self.etsy_auth})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListingCommandView(AuthMixin, RetrieveAPIView):
    serializer_class = ListingSerializer

    def get_queryset(self):
        return Listing.objects.filter(etsy_auth=self.etsy_auth)

    def get(self, request, *args, **kwargs):
        cmd = kwargs.get("cmd")
        listing = self.get_object()
        if cmd == "upload":
            listing.upload_to_etsy()
        elif cmd == "update":
            listing.update_in_etsy()
            
        return super().get(request, *args, **kwargs)



class BaseCreateListingFileView(AuthMixin, CreateAPIView):
    """ Base View for Listing Files """
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        listing_id = request.headers.get("x-one-listing-id")
        context = {'listing_id': listing_id, "etsy_auth": self.etsy_auth} 
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class ListingFileCreateView(BaseCreateListingFileView):
    """ Upload a listing file """
    serializer_class = ListingFileSerializer


class ListingImageCreateView(BaseCreateListingFileView):
    """ Upload a listing image """
    serializer_class = ListingImageSerializer



class ListingFileDetailView(AuthMixin, RetrieveUpdateAPIView):
    serializer_class = ListingFileSerializer

    def get_queryset(self):
        return ListingFile.objects.filter(listing__etsy_auth=self.etsy_auth)


class ListingImageDetailView(AuthMixin, RetrieveUpdateAPIView):
    serializer_class = ListingImageSerializer

    def get_queryset(self):
        return ListingImage.objects.filter(listing__etsy_auth=self.etsy_auth)
