from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from codebase.base.utils.http import CustomHttpRequest

from ..articles.models import Article
from ..faqs.models import FAQ
from ..pages.models import Page
from .tasks import save_search_query

User = get_user_model()


def search(request: CustomHttpRequest) -> HttpResponse:
    return render(request, "search/index.html", {"page_title": _("Search")})


def hx_seach_results(request: CustomHttpRequest) -> HttpResponse:
    q = request.GET.get("q")
    if q in ["", None]:
        return HttpResponse()

    save_search_query(
        {
            "user": request.user if isinstance(request.user, User) else None,
            "country_code": request.country.code,
            "site": request.extendedsite.site,
            "query": q,
        }
    )

    pages = Page.objects.filter(body__contains=q)
    articles = Article.objects.filter(body__contains=q)
    faqs = FAQ.objects.filter(question__contains=q)
    total = pages.count() + articles.count() + faqs.count()
    context = {
        "pages": pages,
        "articles": articles,
        "faqs": faqs,
        "total": total,
    }
    return render(request, "search/hx_results.html", context)
