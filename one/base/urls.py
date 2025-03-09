from django.urls import path
from django.views.generic.base import TemplateView

from one.articles.views import ArticleDetailView
from one.base.sitemaps import get_sitemaps
from one.home.views import home

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
    path("<slug:slug>/", ArticleDetailView.as_view(), name="article-detail"),
    path("", home, name="home"),
]
