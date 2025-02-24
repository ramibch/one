from django.urls import path

from . import views

urlpatterns = [
    # Refresh tokens (access_token and refresh_token)
    path(
        "refresh",
        views.TokenRefreshView.as_view(),
        name="etsy_api_refresh",
    ),
    # App
    path(
        "app/create",
        views.AppCreateView.as_view(),
        name="etsy_api_app_create",
    ),
    path(
        "app/commercial",
        views.CommercialAppDetailView.as_view(),
        name="etsy_api_app_commercial_detail",
    ),
    # Shop
    path(
        "shop/create",
        views.ShopCreateView.as_view(),
        name="etsy_api_shop_create",
    ),
    path(
        "shop/<int:pk>",
        views.ShopDetailView.as_view(),
        name="etsy_api_shop_detail",
    ),
    # Listing
    path(
        "listing/create",
        views.ListingCreateView.as_view(),
        name="etsy_api_listing_create",
    ),
    path(
        "listing/<int:pk>",
        views.UserListingDetailView.as_view(),
        name="etsy_api_listing_detail",
    ),
    path(
        "listing/<int:pk>/cmd/<str:cmd>",
        views.ListingCommandView.as_view(),
        name="etsy_api_listing_command",
    ),
    # Listing File
    path(
        "listing/file/create",
        views.ListingFileCreateView.as_view(),
        name="etsy_api_listing_file_create",
    ),
    path(
        "listing/file/<int:pk>",
        views.ListingFileDetailView.as_view(),
        name="etsy_api_listing_file_detail",
    ),
    # Listing Image
    path(
        "listing/image/create",
        views.ListingImageCreateView.as_view(),
        name="etsy_api_listing_image_create",
    ),
    path(
        "listing/image/<int:pk>",
        views.ListingImageDetailView.as_view(),
        name="etsy_api_listing_image_detail",
    ),
]
