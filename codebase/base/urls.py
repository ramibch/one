from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.generic.base import TemplateView

from .sitemaps import get_sitemaps
from .views import favicon

urlpatterns = [
    # Sitemaps
    path("sitemap.xml", sitemap, {"sitemaps": get_sitemaps()}, name="sitemap"),
    # Favicon
    path("favicon.ico", favicon, name="favicon"),
    # robots.txt
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="base/robots.txt", content_type="text/plain"
        ),
    ),
]
