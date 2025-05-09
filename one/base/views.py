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
from django_htmx.http import retarget

from one.articles.models import Article
from one.base.utils.http import CustomHttpRequest
from one.dgt.models import DgtTest
from one.faqs.models import FAQ
from one.landing.models import LandingPage
from one.plans.models import Plan
from one.products.models import Product
from one.quiz.models import Quiz
from one.sites.models import SiteType

from .forms import ContactMessageForm
from .tasks import save_search_query

User = get_user_model()


@require_GET
def home_view(request: CustomHttpRequest) -> HttpResponse:
    """
    Landing home page
    """

    match request.site.site_type:
        case SiteType.STANDARD.value:
            try:
                home = LandingPage.objects.get(site=request.site, is_home=True)
                return render(request, "landing/landing_page.html", {"object": home})
            except LandingPage.DoesNotExist:
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

    models_templates = {
        Article: "articles/article_detail.html",
        Product: "products/product_detail.html",
        LandingPage: "landing/landing_page.html",
    }

    for model_class, template_name in models_templates.items():
        try:
            obj = model_class.objects.get(exp)
            return render(request, template_name, {"object": obj})
        except model_class.DoesNotExist:
            pass

    if slug in settings.TOPICS_DICT:
        context = {
            "page_title": settings.TOPICS_DICT[slug],
            "related_articles": Article.objects.filter(main_topic__name=slug),
            "related_products": Product.objects.filter(topics=[slug]),
            "related_landing_pages": LandingPage.objects.filter(
                site__topics=[slug], slug__isnull=False
            ),
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
        qs = super().get_queryset()
        return qs.filter(
            languages__contains=[get_language()],
            main_topic__name__in=self.request.site.topics,
        )


class FAQListView(ListView):
    model = FAQ


class PrivacyView(TemplateView):
    template_name = "base/privacy.html"


class TermsView(TemplateView):
    template_name = "base/terms.html"


class ImpressView(TemplateView):
    template_name = "base/impress.html"


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


def contact_view(request: CustomHttpRequest) -> HttpResponse:
    form = ContactMessageForm(request.POST or None)

    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.client = request.client
            obj.site = request.site
            obj.save()
            msg = _("Thank you for your message. I will reply as soon as I can.")
            return HttpResponse(f"<center> ✅ {msg}</center>")

        res = HttpResponse("⚠️ " + form.errors.as_text())
        return retarget(res, "#errors")

    return render(request, "base/contact.html", {"form": form})


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
