from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from one.base.utils.http import CustomHttpRequest


@require_GET
def home(request: CustomHttpRequest) -> HttpResponse:
    # https://www.youtube.com/watch?v=g3cmNDlwGEg
    if request.user.is_authenticated and hasattr(request.site, "userhome"):
        return userhome(request)
    if hasattr(request.site, "home"):
        obj = request.site.home
    else:
        raise Http404
    return render(request, "home/home.html", {"object": obj})


def userhome(request: CustomHttpRequest) -> HttpResponse:
    return render(request, "home/userhome.html", {"object": request.site.userhome})
