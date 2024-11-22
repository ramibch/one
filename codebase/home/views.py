from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from ..articles.models import Article


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    # https://www.youtube.com/watch?v=g3cmNDlwGEg

    if request.user.is_authenticated:
        userhome = request.extendedsite.userhome
        return render(request, "home/userhome.html", {"object": userhome})

    home = request.extendedsite.home
    context = {"object": home}
    if home.display_last_articles:
        context["last_articles"] = Article.objects.filter()[:5]
    return render(request, "home/home.html", context=context)
