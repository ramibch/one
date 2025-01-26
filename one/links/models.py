from auto_prefetch import ForeignKey, Manager
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from ..base.utils.abstracts import TranslatableModel

DJ_PATHS = (
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
    ("quiz_list", _("English Quizzes")),
)


class LinkManager(Manager):
    def sync_django_paths(self):
        new_links = []
        for url_path in DJ_PATHS:
            if self.filter(django_url_path=url_path[0]).exists():
                continue
            new_links.append(Link(django_url_path=url_path[0]))

        self.bulk_create(new_links)


class Link(TranslatableModel):
    __optional = {"null": True, "blank": True}
    __foreignkey_args = __optional | {"on_delete": models.CASCADE}
    custom_title = models.CharField(max_length=128, **__optional)
    external_url = models.URLField(max_length=256, **__optional)
    django_url_path = models.CharField(max_length=32, choices=DJ_PATHS, **__optional)
    page = ForeignKey("pages.Page", **__foreignkey_args)
    plan = ForeignKey("plans.Plan", **__foreignkey_args)
    article = ForeignKey("articles.Article", **__foreignkey_args)
    topic = ForeignKey("base.Topic", **__foreignkey_args)

    objects: LinkManager = LinkManager()

    def __str__(self):
        return f"<Link to {self.title}>"

    def clean_custom_title(self):
        if self.external_url and self.custom_title is None:
            raise ValidationError(
                _("Enter a custom title if an external url is entered."), code="invalid"
            )

    def clean(self):
        if self.link_fields.count(None) != self.count_link_fields - 1:
            raise ValidationError(_("One link must be entered."), code="invalid")
        super().clean()

    @cached_property
    def model_object_fields(self):
        return [self.page, self.plan, self.article, self.topic]

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
        if self.custom_title:
            return self.custom_title

        if self.django_url_path:
            return self.get_django_url_path_display()

        if self.model_obj:
            return self.model_obj.title
