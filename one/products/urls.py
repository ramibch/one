from django.urls import path

from . import feeds, views

urlpatterns = [
    path("<str:slug>", views.ProductDetailView.as_view(), name="product-detail"),
    # Feeds - produts
    path("pins/products/en", feeds.ProductPinFeed("en")),
    path("pins/products/de", feeds.ProductPinFeed("de")),
    path("pins/products/es", feeds.ProductPinFeed("es")),
    # Feeds - Etsy listings
    path("pins/etsy/en", feeds.EtsyListingPinFeed("en")),
    path("pins/etsy/de", feeds.EtsyListingPinFeed("de")),
    path("pins/etsy/es", feeds.EtsyListingPinFeed("es")),
]
