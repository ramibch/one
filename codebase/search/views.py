from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from ..articles.models import Article
from ..pages.models import Page
from .tasks import save_search_query

User = get_user_model()


def search(request: HttpRequest) -> HttpResponse:
    return render(request, "search/index.html", {"page_title": _("Search")})


def hx_seach_results(request: HttpRequest) -> HttpResponse:
    q = request.GET.get("q")
    if q in ["", None]:
        return HttpResponse()

    save_search_query(
        {
            "user": request.user if isinstance(request.user, User) else None,
            "country_code": request.country.code,
            "site": get_current_site(request),
            "query": q,
        }
    )

    print(get_current_site(request))

    pages = Page.objects.filter(body__contains=q)
    articles = Article.objects.filter(body__contains=q)
    total = pages.count() + articles.count()
    context = {"pages": pages, "articles": articles, "total": total}
    return render(request, "search/hx_results.html", context)
