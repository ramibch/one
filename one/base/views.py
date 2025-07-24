import json
import operator
from functools import reduce

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sitemaps.views import index as django_sitemap_index
from django.contrib.sitemaps.views import sitemap as django_sitemap
from django.db.models import Q
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django_htmx.http import retarget

from one.articles.models import Article
from one.bot import Bot
from one.candidates.views import CandidateDashboardView
from one.choices import Topics
from one.db import TranslatableModel
from one.dgt.views import dgt_test_index
from one.faqs.models import FAQ
from one.landing.models import LandingPage
from one.products.models import Product
from one.quiz.views import quiz_list
from one.sites.models import SiteType

from .forms import ContactMessageForm
from .models import CSPReport
from .tasks import save_search_query

User = get_user_model()


class HomeView(View):
    http_method_names = ["get"]

    def get_landing(self, request):
        try:
            obj = LandingPage.objects.get(site=request.site, is_home=True)
            return render(request, "landing/landing_page.html", {"landing": obj})
        except LandingPage.DoesNotExist as err:
            raise Http404 from err

    def get(self, request, *args, **kwargs):
        site_type = request.site.site_type

        # std site
        if site_type == SiteType.STANDARD:
            return self.get_landing(request)

        # dgt tests
        if site_type == SiteType.DGT:
            return dgt_test_index(request)

        # english quizzes
        if site_type == SiteType.ENGLISH:
            return quiz_list(request)

        # job apps site
        if site_type == SiteType.JOBAPPS and request.user.is_authenticated:
            return CandidateDashboardView.as_view()(request)
        else:
            return self.get_landing(request)


class SlugPageView(View):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        slug = kwargs["slug"]

        slug_dict = {f"slug_{lang}": kwargs["slug"] for lang in settings.LANGUAGE_CODES}
        expr = reduce(
            operator.or_, (Q(**d) for d in [dict([i]) for i in slug_dict.items()])
        )

        models_templates = {
            Article: "articles/article_detail.html",
            Product: "products/product_detail.html",
            LandingPage: "landing/landing_page.html",
        }

        for model_class, template_name in models_templates.items():
            assert issubclass(model_class, TranslatableModel)
            try:
                obj = model_class.objects.get(expr)
                return render(request, template_name, {"object": obj})
            except model_class.DoesNotExist:
                pass

        if slug in Topics.values:
            context = {
                "page_title": Topics(slug).label,
                "related_articles": Article.objects.filter(
                    main_topic__name=slug, slug__isnull=True
                ),
                "related_products": Product.objects.filter(
                    topics=[slug], slug__isnull=True
                ),
                "related_landing_pages": LandingPage.objects.filter(
                    site__topics=[slug], slug__isnull=False
                ),
            }
            return render(request, "base/topic.html", context)

        raise Http404


# Static pages
class PrivacyView(TemplateView):
    template_name = "base/privacy.html"


class TermsView(TemplateView):
    template_name = "base/terms.html"


class RobotTxtView(TemplateView):
    content_type = "text/plain"
    template_name = "robots.txt"


class SearchView(View):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        return render(request, "search/index.html", {"page_title": _("Search")})


class SearchResultsView(View):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
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


class ContactView(FormView):
    http_method_names = ["get", "post"]
    template_name = "base/contact.html"
    form_class = ContactMessageForm

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        initial = {}
        if request.user.is_authenticated:
            initial = {"name": request.user.full_name, "email": request.user.email}
        form = self.form_class(None, initial=initial)
        context = {"form": form}

        return render(request, self.template_name, context)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.client = self.request.client
        obj.site = self.request.site
        obj.save()
        msg = _("Thank you for your message. I will reply as soon as I can.")
        return HttpResponse(f"<center> ✅ {msg}</center>")

    def form_invalid(self, form):
        res = HttpResponse("⚠️ " + form.errors.as_text())
        return retarget(res, "#errors")


@require_GET
@cache_control(max_age=60 * 60 * 24 * 30, immutable=True, public=True)  # 30 days
def favicon_view(request) -> HttpResponse:
    emoji = request.site.emoji or "🌐"
    return HttpResponse(
        (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            + f'<text y=".9em" font-size="90">{emoji}</text>'
            + "</svg>"
        ),
        content_type="image/svg+xml",
    )


def error_404(request, exception):
    return render(request, "error.html", {"page_title": _("Not found")}, status=404)


def error_403(request, exception):
    return render(
        request, "error.html", {"page_title": _("Request blocked")}, status=403
    )


def error_500(request):
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


@csrf_exempt
def csp_report(request):
    try:
        data = json.loads(request.body.decode("utf-8")).get("csp-report", {})
        CSPReport.objects.get_or_create(
            violated_directive=data.get("violated-directive"),
            effective_directive=data.get("effective-directive"),
            blocked_uri=data.get("blocked-uri"),
            document_uri=data.get("document-uri"),
            source_file=data.get("source-file"),
            line_number=data.get("line-number"),
            column_number=data.get("column-number"),
            defaults={
                "disposition": data.get("disposition"),
                "original_policy": data.get("original-policy"),
                "referrer": data.get("referrer"),
                "status_code": data.get("status-code"),
            },
        )
    except Exception as e:
        Bot.to_admin(f"Failed to save CSP report: {e}")
    return JsonResponse({"status": "ok"})
