from django.urls import path

from . import feeds

urlpatterns = [
    # Feeds
    path("pins/etsy/en", feeds.EtsyProductPinFeed("en")),
    path("pins/etsy/de", feeds.EtsyProductPinFeed("de")),
    path("pins/etsy/es", feeds.EtsyProductPinFeed("es")),
]
