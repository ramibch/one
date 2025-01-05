from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.generic.base import TemplateView

from .feeds import RssArticleFeeds, RssListingFeeds
from .sitemaps import get_sitemaps
from .views import favicon, feedback, home, hx_seach_results, page_detail, search

urlpatterns = [
    # home
    path("", home, name="home"),
    path("feedback", feedback, name="feedback"),
    # sitemap
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": get_sitemaps()},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # robots.txt
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path("favicon.ico", favicon, name="favicon"),
    # rss feeds
    path("feed/rss/listings", RssListingFeeds(), name="feed-rss-listings"),
    path("feed/rss/articles", RssArticleFeeds(), name="feed-rss-articles"),
    # search
    path("s/", search, name="search"),
    path("s/results/", hx_seach_results, name="search-results"),
    # page (includes all page objects)
    path("<str:slug>/", page_detail, name="page-detail"),
]
