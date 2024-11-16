from auto_prefetch import ForeignKey, Model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from ..articles.models import Article
from ..pages.models import Page
from ..plans.models import Plan

DJANGO_URL_PATHS = (
    # Only url paths without path arguments
    ("home", _("Home")),
    ("search", _("Search")),
    ("sitemap", _("Sitemap")),
    ("article_list", _("Articles")),
    ("plan_list", _("Plans")),
    ("account_login", _("Sign In")),
    ("account_signup", _("Sign Up")),
    ("user_dashboard", _("Account")),
    ("faq_list", _("FAQs")),
)


class Link(Model):
    custom_title = models.CharField(max_length=128, null=True, blank=True)
    external_url = models.URLField(max_length=256, null=True, blank=True)
    django_url_path = models.CharField(blank=True, null=True, max_length=32, choices=DJANGO_URL_PATHS)
    page = ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    plan = ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True)
    article = ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    allow_field_translation = models.BooleanField(default=False)

    def __str__(self):
        return f"<Link to {self.title}>"

    def clean_custom_title(self):
        if self.external_url and self.custom_title is None:
            raise ValidationError(_("Enter a custom title if an external url is entered."), code="invalid")

    def clean(self):
        if self.link_fields.count(None) != self.count_link_fields - 1:
            raise ValidationError(_("One link must be entered."), code="invalid")
        super().clean()

    @cached_property
    def model_object_fields(self):
        return [self.page, self.plan, self.article]

    @cached_property
    def other_link_fields(self):
        return [self.django_url_path, self.external_url]

    @cached_property
    def link_fields(self):
        return self.model_object_fields + self.other_link_fields

    @cached_property
    def count_link_fields(self):
        return len(self.link_fields)

    @cached_property
    def model_obj(self):
        return next((obj for obj in self.model_object_fields if obj is not None), None)

    @cached_property
    def url(self):
        if self.django_url_path:
            return reverse_lazy(self.django_url_path)

        if self.external_url:
            return self.external_url

        if self.model_obj:
            return self.model_obj.url

    @cached_property
    def title(self):
        if self.django_url_path:
            return self.get_django_url_path_display()

        if self.custom_title:
            return self.custom_title

        if self.model_obj:
            return self.model_obj.title

    def get_link_from_path(path):
        pass


def create_initial_django_links():
    links = []
    for url_path in DJANGO_URL_PATHS:
        if Link.objects.filter(django_url_path=url_path[0]).exists():
            continue
        links.append(Link(django_url_path=url_path[0]))

    return Link.objects.bulk_create(links)
