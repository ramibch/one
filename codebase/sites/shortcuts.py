from django.apps import apps

from .requests import RequestSite


def get_current_site(request):
    """
    Check if sites is installed and return either the current
    ``Site`` object or a ``RequestSite`` object based on the request.
    """
    # Import is inside the function because its point is to avoid importing the
    # Site models when codebase.sites isn't installed.
    if apps.is_installed("codebase.sites"):
        from .models import Site

        return Site.objects.get_current(request)
    else:
        return RequestSite(request)
