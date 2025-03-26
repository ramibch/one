from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView

from one.articles.views import ArticleDetailView
from one.home.views import home

from . import sitemaps
from .views import favicon, hx_search_results_view, search_view, sitemap


def get_sitemaps(*args, **kwargs):
    return {
        "articles": sitemaps.ArticleSitemap(),
        "tools": sitemaps.ToolSitemap(),
    }


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
    # Search
    path(_("search"), search_view, name="search-page"),
    path("hx-search-results", hx_search_results_view, name="search-results"),
    # Test
    path(_("translate-this-url"), search_view, name="translate-url"),
    # TODO: page url (Topic, Article, Product, ...)
    path("<slug:slug>", ArticleDetailView.as_view(), name="article-detail"),
    # Home
    path("", home, name="home"),
]
