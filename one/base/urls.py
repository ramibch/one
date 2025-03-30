from django.urls import path
from django.utils.translation import gettext_lazy as _

from .sitemaps import get_sitemaps
from .views import (
    ArticleDetailView,
    ArticleListView,
    FAQListView,
    PlanDetailView,
    PlanListView,
    ProductListView,
    RobotTxtView,
    dispatch_home_view,
    favicon_view,
    hx_search_results_view,
    search_view,
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
    path(_("search"), search_view, name="search"),
    path("hx-search-results", hx_search_results_view, name="search-results"),
    # Article list
    path(_("articles"), ArticleListView.as_view(), name="article_list"),
    # Plan list
    path(_("plans"), PlanListView.as_view(), name="plan_list"),
    path(_("plan") + "/<slug:slug>/", PlanDetailView.as_view(), name="plan_detail"),
    # Product list
    path(_("products"), ProductListView.as_view(), name="plan_list"),
    # FAQ list
    path(_("faqs"), FAQListView.as_view(), name="faq_list"),
    # TODO: page url (Topic, Article, Product, ...)
    path("<slug:slug>", ArticleDetailView.as_view(), name="article-detail"),
    # Home
    path("", dispatch_home_view, name="home"),
]
