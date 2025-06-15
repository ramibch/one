from auto_prefetch import ForeignKey, Manager
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from one.choices import Topics
from one.db import ChoiceArrayField, OneModel, TranslatableModel

from .animations import (
    AnimationDelay,
    AnimationRepeat,
    AnimationSpeed,
    AnimationType,
    AttentionSeekers,
)

User = get_user_model()


class SearchTerm(OneModel):
    query = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    client = ForeignKey("clients.Client", null=True, on_delete=models.SET_NULL)
    site = ForeignKey("sites.Site", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.query


class ContactMessage(OneModel):
    client = ForeignKey(
        "clients.Client",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    site = ForeignKey(
        "sites.Site",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(_("Your name"), max_length=128)
    email = models.EmailField(_("Email address"), max_length=128)
    message = models.TextField(_("Message"), max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name}  <{self.email}>"


class Animation(OneModel):
    animation_type = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        default=AnimationType.VANILLA,
        choices=AnimationType.choices,
    )
    name = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        default=AttentionSeekers.FLASH,
        choices=AttentionSeekers.choices,
    )
    repeat = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        default=AnimationRepeat.ONE,
        choices=AnimationRepeat.choices,
    )
    speed = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=AnimationSpeed.choices,
    )
    delay = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=AnimationDelay.choices,
    )


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
    ("privacy", _("Privacy Policy")),
    ("terms", _("Terms and Conditions")),
    ("impress", _("Impress")),
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
        choices=Topics,
    )

    landing = ForeignKey(
        "landing.LandingPage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    product = ForeignKey(
        "products.Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    objects: LinkManager = LinkManager()

    def __str__(self):
        return f"<Link to {self.title}>"

    def clean(self):
        ext_url = self.external_url

        if self.link_fields.count(None) != len(self.link_fields) - 1:
            raise ValidationError(_("One link must be entered."), code="invalid")

        if ext_url and self.custom_title is None:
            raise ValidationError(_("Custom title is required."), code="invalid")

        if ext_url and Link.objects.filter(external_url=ext_url).exists():
            raise ValidationError(_("External url already exists."), code="invalid")

        if self.url_path and Link.objects.filter(url_path=self.url_path).exists():
            raise ValidationError(_("Url path already exists."), code="invalid")

        if self.topic and Link.objects.filter(topic=self.topic).exists():
            raise ValidationError(_("Topic link already exists."), code="invalid")

        if self.landing and Link.objects.filter(landing=self.landing).exists():
            raise ValidationError(_("Landing link already exists."), code="invalid")

        if self.product and Link.objects.filter(product=self.product).exists():
            raise ValidationError(_("Product link already exists."), code="invalid")

        return super().clean()

    @cached_property
    def link_fields(self):
        return [
            self.url_path,
            self.external_url,
            self.topic,
            self.landing,
            self.product,
        ]

    @cached_property
    def url_and_title(self) -> tuple[str, str]:
        if self.url_path:
            return reverse_lazy(self.url_path), self.get_url_path_display()

        if self.external_url:
            return self.external_url, self.custom_title

        if self.topic:
            return f"/{self.topic}", self.get_topic_display()

        if self.landing:
            return self.landing.url, self.landing.title

        if self.product:
            return self.product.url, self.product.title

        return "#", ""

    @cached_property
    def url(self) -> str:
        return self.url_and_title[0]

    @cached_property
    def title(self) -> str:
        return self.url_and_title[1]
