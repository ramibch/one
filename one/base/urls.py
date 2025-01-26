from django.urls import path
from django.views.generic.base import TemplateView

from one.base.sitemaps import get_sitemaps

from .views import favicon, sitemap

urlpatterns = [
    # Sitemaps
    path(
        "<str:lang>/sitemap.xml", sitemap, {"sitemaps": get_sitemaps()}, name="sitemap"
    ),
    path("sitemap.xml", sitemap, {"sitemaps": get_sitemaps()}, name="sitemap"),
    # Favicon
    path("favicon.ico", favicon, name="favicon"),
    # robots.txt
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]
