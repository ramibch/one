from auto_prefetch import Manager
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from one.base.utils.abstracts import TranslatableModel
from one.base.utils.db import ChoiceArrayField

PATH_NAMES = (
    # Only url paths without path arguments
    ("home", _("Home")),
    ("search", _("Search")),
    ("sitemap", _("Sitemap")),
    ("contact", _("Contact")),
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
        for url_path in PATH_NAMES:
            if self.filter(url_path=url_path[0]).exists():
                continue
            new_links.append(Link(url_path=url_path[0]))

        self.bulk_create(new_links)


class Link(TranslatableModel):
    LANG_ATTR = "language"
    LANGS_ATTR = "languages"
    language = models.CharField(
        max_length=4,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
    )
    languages = ChoiceArrayField(
        models.CharField(max_length=8, choices=settings.LANGUAGES),
        default=list,
        blank=True,
    )
    custom_title = models.CharField(max_length=128, null=True, blank=True)
    external_url = models.URLField(max_length=256, null=True, blank=True)
    url_path = models.CharField(
        max_length=32,
        choices=PATH_NAMES,
        null=True,
        blank=True,
    )
    topic = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        choices=settings.TOPICS,
    )

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

        if self.external_url and self.custom_title is None:
            raise ValidationError(_("Custom title is required."), code="invalid")

        super().clean()

    @cached_property
    def link_fields(self):
        return [self.url_path, self.external_url, self.topic]

    @cached_property
    def count_link_fields(self):
        return len(self.link_fields)

    @cached_property
    def url_and_title(self):
        if self.url_path:
            return reverse_lazy(self.url_path), self.get_url_path_display()

        if self.external_url:
            return self.external_url, self.custom_title

        if self.topic:
            return f"/{self.topic}", self.get_topic_display()

        return "#", ""  # TODO: Improve this

    @cached_property
    def url(self):
        return self.url_and_title[0]

    @cached_property
    def title(self):
        return self.url_and_title[1]
