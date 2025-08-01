from django.urls import path

from .sitemaps import get_sitemaps
from .views import (
    ContactView,
    HomeView,
    PrivacyView,
    RobotTxtView,
    SearchResultsView,
    SearchView,
    SlugPageView,
    TermsView,
    csp_report,
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
    path("search", SearchView.as_view(), name="search"),
    path("hx-search-results", SearchResultsView.as_view(), name="search-results"),
    # Contact
    path("contact", ContactView.as_view(), name="contact"),
    # "static" pages
    path("~/p", PrivacyView.as_view(), name="privacy"),
    path("~/t", TermsView.as_view(), name="terms"),
    # csp-report
    path("csp-report/", csp_report, name="csp_report"),
    # Article, Product, topic ...
    path("<slug:slug>", SlugPageView.as_view(), name="slug_page"),
    # Home
    path("", HomeView.as_view(), name="home"),
]
