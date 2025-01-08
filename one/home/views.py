from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from one.base.utils.http import CustomHttpRequest


@require_GET
def home(request: CustomHttpRequest) -> HttpResponse:
    # https://www.youtube.com/watch?v=g3cmNDlwGEg
    if hasattr(request.site, "home"):
        return render(request, "home/home.html", {"object": request.site.home})
    else:
        raise Http404
