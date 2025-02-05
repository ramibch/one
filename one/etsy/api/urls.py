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
    # Listing
    path(
        "listing/<pk>",
        views.UserListingDetailView.as_view(),
        name="etsy_api_listing_detail",
    ),
    path(
        "listing/create",
        views.UserListingCreateView.as_view(),
        name="etsy_api_listing_create",
    ),
    # Listing File
    path(
        "listing/file/create",
        views.UserListingFileCreateView.as_view(),
        name="etsy_api_listing_file_create",
    ),
    path(
        "listing/file/<pk>",
        views.UserListingFileDetailView.as_view(),
        name="etsy_api_listing_file_detail",
    ),
    # Listing Image
    path(
        "listing/image/create",
        views.UserListingImageCreateView.as_view(),
        name="etsy_api_listing_image_create",
    ),
    path(
        "listing/image/<pk>",
        views.UserListingImageDetailView.as_view(),
        name="etsy_api_listing_image_detail",
    ),
]
