from django.urls import path
from django.utils.translation import gettext_lazy as _

from .sitemaps import get_sitemaps
from .views import (
    ContactView,
    HomeView,
    ImpressView,
    PrivacyView,
    RobotTxtView,
    SearchResultsView,
    SearchView,
    SlugPageView,
    TermsView,
    favicon_view,
    sitemap_view,
)

urlpatterns = [
    # Sitemaps
    path("<str:lang>/sitemap.xml", sitemap_view, {"sitemaps": get_sitemaps()}),
    path("sitemap.xml", sitemap_view, {"sitemaps": get_sitemaps()}, "sitemap"),
    # Favicon
    path("favicon.ico", favicon_view, name="favicon"),
    # robots.txt
    path("robots.txt", RobotTxtView.as_view()),
    # Search
    path(_("search"), SearchView.as_view(), name="search"),
    path("hx-search-results", SearchResultsView.as_view(), name="search-results"),
    # Contact
    path(_("contact"), ContactView.as_view(), name="contact"),
    # "static" pages
    path("~/p", PrivacyView.as_view(), name="privacy"),
    path("~/t", TermsView.as_view(), name="terms"),
    path("~/i", ImpressView.as_view(), name="impress"),
    # Article, Product, topic ...
    path("<slug:slug>", SlugPageView.as_view(), name="slug_page"),
    # Home
    path("", HomeView.as_view(), name="home"),
]
