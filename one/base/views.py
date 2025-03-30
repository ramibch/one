import importlib

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sitemaps.views import index as django_sitemap_index
from django.contrib.sitemaps.views import sitemap as django_sitemap
from django.db.models import QuerySet
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from one.base.utils.generic_views import MultilinguageDetailView
from one.base.utils.http import CustomHttpRequest
from one.base.utils.telegram import Bot

from ..articles.models import Article
from ..faqs.models import FAQ
from ..plans.models import Plan
from ..products.models import Product
from .tasks import save_search_query

User = get_user_model()


@require_GET
def dispatch_home_view(request: CustomHttpRequest) -> HttpResponse:
    home = getattr(request.site, "home", None)

    if not home or not getattr(home, "view_type", "").strip():
        raise Http404("Home view is not configured.")

    try:
        module_name, _, view_name = home.view_type.rpartition(".")
        view_module = importlib.import_module(module_name)
        view_func = getattr(view_module, view_name)
    except (ModuleNotFoundError, AttributeError, ValueError) as err:
        msg = "Requested view not found."
        Bot.to_admin(f"{msg}.\nhome:{home}\nsite:{request.site}")
        raise Http404(msg) from err

    return view_func(request)


def slug_page_view(request: CustomHttpRequest) -> HttpResponse:
    # TODO: Page, Article, Product, ...
    pass


class ArticleDetailView(MultilinguageDetailView):
    # TODO: Remove
    model = Article


class PlanDetailView(MultilinguageDetailView):
    model = Plan


class ProductDetailView(MultilinguageDetailView):
    model = Product


class ProductListView(ListView):
    model = Product


class PlanListView(ListView):
    model = Plan


class ArticleListView(ListView):
    model = Article

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(languages__contains=[get_language()])


class FAQListView(ListView):
    model = FAQ


def search_view(request: CustomHttpRequest) -> HttpResponse:
    return render(request, "search/index.html", {"page_title": _("Search")})


def hx_search_results_view(request: CustomHttpRequest) -> HttpResponse:
    q = request.GET.get("q")
    if q in ["", None]:
        return HttpResponse()

    save_search_query(
        {
            "user": request.user if isinstance(request.user, User) else None,
            "client": request.client,
            "site": request.site,
            "query": q,
        }
    )

    articles = Article.objects.filter(body__contains=q)
    faqs = FAQ.objects.filter(question__contains=q)
    total = articles.count() + faqs.count()
    context = {
        "articles": articles,
        "products": [],
        "faqs": faqs,
        "total": total,
    }
    return render(request, "search/hx_results.html", context)


@require_GET
@cache_control(max_age=60 * 60 * 24 * 30, immutable=True, public=True)  # 30 days
def favicon_view(request: CustomHttpRequest) -> HttpResponse:
    try:
        emoji = request.site.emoji
    except AttributeError:
        emoji = "🌐"

    return HttpResponse(
        (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            + f'<text y=".9em" font-size="90">{emoji}</text>'
            + "</svg>"
        ),
        content_type="image/svg+xml",
    )


class RobotTxtView(TemplateView):
    content_type = "text/plain"
    template_name = "robots.txt"


def error_404(request: CustomHttpRequest, exception):
    return render(
        request,
        "error.html",
        {"page_title": _("Page not found")},
        status=404,
    )


def error_500(request: CustomHttpRequest):
    return render(
        request,
        "error.html",
        {"page_title": _("Internal Server Error")},
        status=500,
    )


def sitemap_index(*args, **kwargs):
    # https://stackoverflow.com/questions/9817856/django-sitemaps-get-only-pages-of-the-current-website
    for key in kwargs.get("sitemaps", {}):
        kwargs["sitemaps"][key].request = args[0]
        kwargs["sitemaps"][key].lang = kwargs.get("lang", settings.LANGUAGE_CODE)
    kwargs.pop("lang", None)
    return django_sitemap_index(*args, **kwargs)


def sitemap_view(*args, **kwargs):
    # https://stackoverflow.com/questions/9817856/django-sitemaps-get-only-pages-of-the-current-website
    for key in kwargs.get("sitemaps", {}):
        kwargs["sitemaps"][key].request = args[0]
        kwargs["sitemaps"][key].lang = kwargs.get("lang", settings.LANGUAGE_CODE)
    kwargs.pop("lang", None)
    return django_sitemap(*args, **kwargs)
