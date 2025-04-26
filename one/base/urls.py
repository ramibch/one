from django.urls import path
from django.utils.translation import gettext_lazy as _

from .sitemaps import get_sitemaps
from .views import (
    ArticleListView,
    FAQListView,
    ImpressView,
    PlanListView,
    PrivacyView,
    ProductListView,
    RobotTxtView,
    TermsView,
    contact_view,
    favicon_view,
    hx_search_results_view,
    landing_home_view,
    search_view,
    sitemap_view,
    slug_page_view,
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
    # Contact
    path(_("contact"), contact_view, name="contact"),
    path(_("contact") + "/", contact_view),
    path("feedback", contact_view, name="contact-feedback"),
    path("feedback/", contact_view),
    # Article list
    path(_("articles"), ArticleListView.as_view(), name="article_list"),
    # Plan list
    path(_("plans"), PlanListView.as_view(), name="plan_list"),
    # Product list
    path(_("products"), ProductListView.as_view(), name="plan_list"),
    # FAQ list
    path("faqs", FAQListView.as_view(), name="faq_list"),
    # "static" pages
    path("~/p", PrivacyView.as_view(), name="privacy"),
    path("~/t", TermsView.as_view(), name="terms"),
    path("~/i", ImpressView.as_view(), name="impress"),
    # Article, Product, topic ...
    path("<slug:slug>", slug_page_view, name="page-detail"),
    # Home
    path("", landing_home_view, name="home"),
]
