from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from ..articles.models import Article


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    # https://www.youtube.com/watch?v=g3cmNDlwGEg

    site = get_current_site(request)
    context = {}

    if request.user.is_authenticated and False:  # remove False  # noqa: SIM222, SIM223
        template = "home/home.html"
        home = site.userhomepage_set.filter(is_active=True).first()
    else:
        template = "home/home.html"
        home = site.homepage_set.filter(is_active=True).first()
        if getattr(home, "show_last_articles", None):
            context["last_articles"] = Article.objects.filter()[:5]

    context["object"] = home
    return render(request, template, context=context)
