from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from ..articles.models import Article
from ..pages.models import Page


def search(request: HttpRequest) -> HttpResponse:
    return render(request, "search/index.html", {"page_title": _("Search")})


def hx_seach_results(request: HttpRequest) -> HttpResponse:
    q = request.GET.get("q")
    if q in ["", None]:
        return HttpResponse()

    pages = Page.objects.filter(body__contains=q)
    articles = Article.objects.filter(body__contains=q)
    total = pages.count() + articles.count()
    context = {"pages": pages, "articles": articles, "total": total}
    return render(request, "search/hx_results.html", context)
