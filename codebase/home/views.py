from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from ..articles.models import Article


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    # https://www.youtube.com/watch?v=g3cmNDlwGEg

    if request.user.is_authenticated:
        context = {}
        return render(request, "home/user_home.html", context=context)
    else:
        context = {
            "featured_articles": Article.objects.filter(featured=True),
        }
        return render(request, "home/home.html", context=context)
