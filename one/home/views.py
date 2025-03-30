from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def home_view(request) -> HttpResponse:
    """
    Home page of a site

    Check out this video to implemtent the sections:
    https://www.youtube.com/watch?v=g3cmNDlwGEg
    """
    home = request.site.home
    return render(request, home.template_name, {"object": home})
