from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from ..articles.models import Article
from ..pages.models import Page
from .views import favicon, home, hx_seach_results, search

articles_sitemap = {
    "queryset": Article.objects.filter(),
    "date_field": "updated_on",
}

pages_sitemap = {
    "queryset": Page.objects.filter(),
    "date_field": "updated_on",
}

sitemaps = {
    "articles": GenericSitemap(articles_sitemap, priority=0.7),
    "pages": GenericSitemap(pages_sitemap, priority=0.5),
}


urlpatterns = [
    # sitemaps
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # search
    path("s/", search, name="search"),
    path("s/results/", hx_seach_results, name="search-results"),
    path("favicon.ico", favicon, name="favicon"),
    path("", home, name="home"),
]
