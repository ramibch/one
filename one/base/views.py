import operator
from functools import reduce

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sitemaps.views import index as django_sitemap_index
from django.contrib.sitemaps.views import sitemap as django_sitemap
from django.db.models import Q, QuerySet
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from one.articles.models import Article
from one.base.utils.http import CustomHttpRequest
from one.dgt.models import DgtTest
from one.faqs.models import FAQ
from one.home.models import Home
from one.plans.models import Plan
from one.products.models import Product
from one.quiz.models import Quiz
from one.sites.models import SiteType

from .tasks import save_search_query

User = get_user_model()


@require_GET
def home_view(request: CustomHttpRequest) -> HttpResponse:
    """
    Home page
    """

    match request.site.site_type:
        case SiteType.STANDARD.value:
            try:
                home = Home.objects.get(site=request.site)
                return render(request, "home/home.html", {"object": home})
            except Home.DoesNotExist:
                pass

        case SiteType.DGT.value:
            context = {"tests": DgtTest.objects.all()}
            return render(request, "dgt/index.html", context)

        case SiteType.ENGLISH.value:
            context = {"quiz_list": Quiz.objects.all()}
            return render(request, "quiz/quiz_list.html", context)

    raise Http404


def slug_page_view(request: CustomHttpRequest, slug) -> HttpResponse:
    params = {f"slug_{lang_code}": slug for lang_code in settings.LANGUAGE_CODES}
    exp = reduce(operator.or_, (Q(**d) for d in [dict([i]) for i in params.items()]))

    try:
        obj = Article.objects.get(exp)
        return render(request, "articles/article_detail.html", {"object": obj})
    except Article.DoesNotExist:
        pass

    try:
        obj = Product.objects.get(exp)
        return render(request, "products/product_detail.html", {"object": obj})
    except Product.DoesNotExist:
        pass

    if slug in settings.TOPICS_DICT:
        context = {
            "page_title": settings.TOPICS_DICT[slug],
            "related_articles": Article.objects.filter(main_topic__name=slug),
            "related_products": Product.objects.filter(topics=[slug]),
        }
        return render(request, "base/topic.html", context)

    raise Http404


class ProductListView(ListView):
    model = Product


class PlanListView(ListView):
    model = Plan


class ArticleListView(ListView):
    model = Article

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(languages__contains=[get_language()])


class FAQListView(ListView):
    model = FAQ


def search_view(request: CustomHttpRequest) -> HttpResponse:
    return render(request, "search/index.html", {"page_title": _("Search")})


def hx_search_results_view(request: CustomHttpRequest) -> HttpResponse:
    q = request.GET.get("q")
    if q in ["", None]:
        return HttpResponse()

    save_search_query({"client": request.client, "site": request.site, "query": q})

    articles = Article.objects.filter(body__contains=q)
    faqs = FAQ.objects.filter(question__contains=q)
    total = articles.count() + faqs.count()
    context = {
        "articles": articles,
        "products": [],
        "faqs": faqs,
        "total": total,
    }
    return render(request, "search/hx_results.html", context)


@require_GET
@cache_control(max_age=60 * 60 * 24 * 30, immutable=True, public=True)  # 30 days
def favicon_view(request: CustomHttpRequest) -> HttpResponse:
    emoji = request.site.emoji or "🌐"
    return HttpResponse(
        (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            + f'<text y=".9em" font-size="90">{emoji}</text>'
            + "</svg>"
        ),
        content_type="image/svg+xml",
    )


class RobotTxtView(TemplateView):
    content_type = "text/plain"
    template_name = "robots.txt"


def error_404(request: CustomHttpRequest, exception):
    return render(request, "error.html", {"page_title": _("Not found")}, status=404)


def error_500(request: CustomHttpRequest):
    return render(request, "error.html", {"page_title": _("Server Error")}, status=500)


def sitemap_index(*args, **kwargs):
    # https://stackoverflow.com/questions/9817856/django-sitemaps-get-only-pages-of-the-current-website
    for key in kwargs.get("sitemaps", {}):
        kwargs["sitemaps"][key].request = args[0]
        kwargs["sitemaps"][key].lang = kwargs.get("lang", settings.LANGUAGE_CODE)
    kwargs.pop("lang", None)
    return django_sitemap_index(*args, **kwargs)


def sitemap_view(*args, **kwargs):
    # https://stackoverflow.com/questions/9817856/django-sitemaps-get-only-pages-of-the-current-website
    for key in kwargs.get("sitemaps", {}):
        kwargs["sitemaps"][key].request = args[0]
        kwargs["sitemaps"][key].lang = kwargs.get("lang", settings.LANGUAGE_CODE)
    kwargs.pop("lang", None)
    return django_sitemap(*args, **kwargs)
