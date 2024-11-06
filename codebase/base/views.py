from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from ..utils.telegram import Bot


@require_GET
@cache_control(max_age=60 * 60 * 24 * 30, immutable=True, public=True)  # 30 days
def favicon(request: HttpRequest) -> HttpResponse:
    try:
        emoji = get_current_site(request).siteprofile.emoji
    except AttributeError:
        emoji = "🌐 "

    return HttpResponse(
        ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">' + f'<text y=".9em" font-size="90">{emoji}</text>' + "</svg>"),
        content_type="image/svg+xml",
    )


def error_404(request, exception):
    Bot.to_admin(f"404 Error: {exception}\n\n{request}\n{request.user}")
    return render(request, "error.html", {"page_title": _("Page not found")}, status=404)


def error_500(request):
    Bot.to_admin(f"500 Error: {request}\n{request.user}")
    return render(request, "error.html", {"page_title": _("Internal Server Error")}, status=500)
