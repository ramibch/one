from django.urls import path

from . import feeds, views

urlpatterns = [
    path("<str:slug>", views.ProductDetailView.as_view(), name="product-detail"),
    # Feeds
    path("pins/etsy/en", feeds.EtsyProductPinFeed("en")),
    path("pins/etsy/de", feeds.EtsyProductPinFeed("de")),
    path("pins/etsy/es", feeds.EtsyProductPinFeed("es")),
]
