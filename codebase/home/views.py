from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET

from ..articles.models import Article


@require_GET
@cache_page(60 * 60 * 24 * 1)
def home(request: HttpRequest) -> HttpResponse:
    # https://www.youtube.com/watch?v=g3cmNDlwGEg
    context = {
        "featured_articles": Article.objects.filter(featured=True),
    }
    return render(request, "home/home.html", context=context)
