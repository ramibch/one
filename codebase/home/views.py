from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from codebase.base.utils.http import CustomHttpRequest


@require_GET
def home(request: CustomHttpRequest) -> HttpResponse:
    # https://www.youtube.com/watch?v=g3cmNDlwGEg

    name = "userhome" if request.user.is_authenticated else "home"
    home = getattr(request.site, name)
    return render(request, f"home/{name}.html", {"object": home})
