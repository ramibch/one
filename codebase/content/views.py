from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_control, cache_page
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET

from .forms import FeedbackForm
from .models import (
    Article,
    Home,
    ListingProduct,
    Page,
    SearchTerm,
    get_page_object,
)


@cache_page(60 * 60 * 24 * 1)
@csrf_protect
def home(request):
    lang = get_language()
    try:
        obj = Home.objects.get(language=lang)
    except Home.DoesNotExist:
        obj = Home.objects.get(language=settings.LANGUAGE_CODE)

    return render(request, "home.html", {"object": obj})


def page_detail(request, slug):
    obj = get_page_object(slug)
    if obj is None or not getattr(obj, "public", False):
        raise Http404
    context = {"object": obj}
    return render(request, obj.template_name, context)


@cache_page(60 * 60 * 24 * 1)
def search(request):
    return render(request, "search/main.html")


def hx_seach_results(request):
    q = request.GET.get("q")
    if q == "":
        return HttpResponse()

    try:
        SearchTerm.objects.create(q=q)
    except Exception:
        pass

    pages = Page.objects.filter(body__contains=q, public=True)
    products = ListingProduct.objects.filter(dirname__contains=q)
    articles = Article.objects.filter(body__contains=q, public=True)
    total = pages.count() + products.count() + articles.count()
    context = {
        "pages": pages,
        "products": products,
        "articles": articles,
        "total": total,
    }
    return render(request, "search/results.html", context)


@require_GET
@cache_control(max_age=60 * 60 * 24 * 30, immutable=True, public=True)  # 30 days
def favicon(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            + '<text y=".9em" font-size="90">📝</text>'
            + "</svg>"
        ),
        content_type="image/svg+xml",
    )


def feedback(request):
    form = FeedbackForm(request.POST or None)

    if request.method == "GET":
        context = {"form": form}
        return render(request, "feedback.html", context)
    elif request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("✅ " + _("Thank you for your message!"))

        return HttpResponse("⚠️ " + form.errors.as_text() + " ⚠️")
