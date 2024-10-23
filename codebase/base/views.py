from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control, cache_page
from django.views.decorators.http import require_GET

from ..articles.models import Article
from ..pages.models import Page


@cache_page(60 * 60 * 24 * 1)
def home(request: HttpRequest) -> HttpResponse:
    context = {"featured_articles": Article.objects.filter(featured=True), "page_title": settings.WEBSITE_NAME}
    return render(request, "base/home.html", context=context)


@require_GET
@cache_control(max_age=60 * 60 * 24 * 30, immutable=True, public=True)  # 30 days
def favicon(request: HttpRequest) -> HttpResponse:
    emoji = getattr(settings, "WEBSITE_EMOJI", "🌐")

    return HttpResponse(
        ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">' + f'<text y=".9em" font-size="90">{emoji}</text>' + "</svg>"),
        content_type="image/svg+xml",
    )


@cache_page(60 * 60 * 24 * 1)
def search(request: HttpRequest) -> HttpResponse:
    return render(request, "base/search.html")


@cache_page(60 * 60 * 24 * 1)
def hx_seach_results(request: HttpRequest) -> HttpResponse:
    q = request.GET.get("q")
    if q == "":
        return HttpResponse()

    pages = Page.objects.filter(body__contains=q)
    articles = Article.objects.filter(body__contains=q)
    total = pages.count() + articles.count()
    context = {"pages": pages, "articles": articles, "total": total}
    return render(request, "base/hx_search_results.html", context)
