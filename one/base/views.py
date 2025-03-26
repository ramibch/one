from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sitemaps.views import index as django_sitemap_index
from django.contrib.sitemaps.views import sitemap as django_sitemap
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from one.base.utils.http import CustomHttpRequest

from ..articles.models import Article
from ..faqs.models import FAQ
from .tasks import save_search_query

User = get_user_model()


def slug_page_view(request: CustomHttpRequest) -> HttpResponse:
    # TODO: Page, Article, Product, ...
    pass


@require_GET
@cache_control(max_age=60 * 60 * 24 * 30, immutable=True, public=True)  # 30 days
def favicon(request: CustomHttpRequest) -> HttpResponse:
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


def sitemap(*args, **kwargs):
    # https://stackoverflow.com/questions/9817856/django-sitemaps-get-only-pages-of-the-current-website
    for key in kwargs.get("sitemaps", {}):
        kwargs["sitemaps"][key].request = args[0]
        kwargs["sitemaps"][key].lang = kwargs.get("lang", settings.LANGUAGE_CODE)
    kwargs.pop("lang", None)
    return django_sitemap(*args, **kwargs)


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
