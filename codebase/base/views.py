from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control, cache_page
from django.views.decorators.http import require_GET
from django.utils.translation import gettext_lazy as _

from ..articles.models import Article
from ..utils.telegram import Bot


@require_GET
@cache_page(60 * 60 * 24 * 1)
def home(request: HttpRequest) -> HttpResponse:
    # https://www.youtube.com/watch?v=g3cmNDlwGEg
    context = {
        "featured_articles": Article.objects.filter(featured=True),
    }
    return render(request, "base/home.html", context=context)


@require_GET
@cache_control(max_age=60 * 60 * 24 * 30, immutable=True, public=True)  # 30 days
def favicon(request: HttpRequest) -> HttpResponse:
    emoji = getattr(settings.WEBSITE, "emoji", "🌐")

    return HttpResponse(
        ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">' + f'<text y=".9em" font-size="90">{emoji}</text>' + "</svg>"),
        content_type="image/svg+xml",
    )


def error_404(request, exception):
    Bot.to_admin(f"404 Error: {exception}\n\n{request}\n{request.user}")
    return render(request, "base/404.html", {"page_title": _("Page not found")}, status=404)


def error_500(request):
    Bot.to_admin(f"500 Error: {request}\n{request.user}")
    return render(request, "base/500.html", {"page_title": _("Internal Server Error")},status=500)
