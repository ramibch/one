from django.contrib.sitemaps.views import sitemap
from django.urls import path

from .sitemaps import get_sitemaps
from .views import favicon, home, hx_seach_results, search

urlpatterns = [
    # Sitemaps
    path("sitemap.xml", sitemap, {"sitemaps": get_sitemaps()}, name="django.contrib.sitemaps.views.sitemap"),
    # Search
    path("s/", search, name="search"),
    path("s/results/", hx_seach_results, name="search-results"),
    # Favicon
    path("favicon.ico", favicon, name="favicon"),
    # Home
    path("", home, name="home"),
]
