from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from one.base.utils.http import CustomHttpRequest

from ..articles.models import Article
from ..faqs.models import FAQ
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
