from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from ..articles.models import Article


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    # https://www.youtube.com/watch?v=g3cmNDlwGEg

    template = "home/home.html"
    site = get_current_site(request)

    context = {
        "featured_articles": Article.objects.filter(featured=True),
        "object": site.homepage_set.filter(is_active=True).first(),
    }

    return render(request, template, context=context)
