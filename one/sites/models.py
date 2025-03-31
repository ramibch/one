import string

from auto_prefetch import Manager, Model
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ManyToManyField, QuerySet
from django.db.models.signals import pre_delete, pre_save
from django.http.request import split_domain_port
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.timezone import timedelta
from django.utils.translation import gettext_lazy as _

from one.base.utils.abstracts import TranslatableModel
from one.base.utils.db import ChoiceArrayField
from one.menus.models import FooterItem, FooterLink, NavbarLink, SocialMediaLink

SITE_CACHE = {}


def _simple_domain_name_validator(value):
    """
    Validate that the given value contains no whitespaces to prevent common
    typos.
    """
    checks = ((s in value) for s in string.whitespace)
    if any(checks):
        raise ValidationError(
            _("The domain name cannot contain any spaces or tabs."),
            code="invalid",
        )


class SiteManager(Manager):
    use_in_migrations = True

    def _get_site_by_request(self, request):
        host = request.get_host()
        try:
            # First attempt to look up the site by host with or without port.
            if host not in SITE_CACHE:
                SITE_CACHE[host] = self.get(domain__iexact=host)
            return SITE_CACHE[host]
        except Site.DoesNotExist:
            # Fallback to looking up site after stripping port from the host.
            domain, port = split_domain_port(host)
            if domain not in SITE_CACHE:
                SITE_CACHE[domain] = self.get(domain__iexact=domain)
            return SITE_CACHE[domain]

    def get_current(self, request):
        return self._get_site_by_request(request)

    def clear_cache(self):
        """Clear the ``Site`` object cache."""
        global SITE_CACHE
        SITE_CACHE = {}


class PicoCssColor(models.TextChoices):
    AMBER = "amber", _("Amber")
    BLUE = "blue", _("Blue")
    FUCHSIA = "fuchsia", _("Fuchsia")
    JADE = "jade", _("Jade")
    GREY = "grey", _("Grey")
    PURPLE = "purple", _("Purple")
    CYAN = "cyan", _("Cyan")
    RED = "red", _("Read")
    VIOLET = "violet", _("Violet")
    INDIGO = "indigo", _("Indigo")
    SLATE = "slate", _("Slate")
    LIME = "lime", _("Lime")
    COLORS = "colors", _("Colors")
    ORANGE = "orange", _("Orange")
    PUMPKIN = "pumpkin", _("Pumpkin")
    ZINC = "zinc", _("Zinc")
    SAND = "sand", _("Sand")
    YELLOW = "yellow", _("Yellow")
    PINK = "pink", _("Pink")
    GREEN = "green", _("Green")


class SiteType(models.TextChoices):
    STANDARD = "standard", _("Standard")
    DGT = "dgt", _("DGT")
    ENGLISH = "english", _("English quizzes")


class Site(TranslatableModel):
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
    site_type = models.CharField(
        max_length=16,
        choices=SiteType.choices,
        default=SiteType.STANDARD,
    )
    domain = models.CharField(
        _("Name"),
        max_length=32,
        unique=True,
        db_index=True,
        validators=[_simple_domain_name_validator],
    )
    remarks = models.TextField(null=True, blank=True)

    # Brand
    brand_name = models.CharField(max_length=32, null=True)
    emoji = models.CharField(max_length=8, null=True, blank=True)
    emoji_in_brand = models.BooleanField(default=True, blank=True)
    picocss_color = models.CharField(
        max_length=16,
        choices=PicoCssColor.choices,
        default=PicoCssColor.PUMPKIN,
    )

    footer_links_separator = models.CharField(max_length=4, default="|")
    change_theme_light_in_footer = models.BooleanField(default=True)
    change_theme_light_in_navbar = models.BooleanField(default=True)
    change_language_in_navbar = models.BooleanField(default=True)
    change_language_in_footer = models.BooleanField(default=True)

    spam_requests_duration = models.DurationField(default=timedelta(days=1))
    requests_duration = models.DurationField(default=timedelta(days=14))

    topics = ManyToManyField("base.Topic", blank=True)

    # SEO
    title = models.CharField(max_length=64, null=True, blank=True)
    description = models.TextField(max_length=256, null=True, blank=True)
    keywords = models.TextField(max_length=256, null=True, blank=True)

    objects = SiteManager()

    def __str__(self):
        return self.domain

    def clean_emoji(self):
        if self.emoji_in_brand and self.emoji in [None, ""]:
            raise ValidationError(_("Add an emoji."), code="invalid")

    @cached_property
    def display_brand(self):
        if self.emoji_in_brand:
            return f"{self.emoji} {self.brand_name}"
        return self.brand_name

    @cached_property
    def picocss_static_file(self) -> str:
        return f"css/picocss/pico.{self.picocss_color}.min.css"

    @cached_property
    def url(self) -> str:
        schema = "https" if settings.HTTPS else "http"
        return f"{schema}://{self.domain}"

    @cached_property
    def from_email_address(self):
        return f"{self.display_brand} <no-reply@{self.domain}>"

    @cached_property
    def topic_keywords(self):
        return ", ".join([t.name for t in self.topics.all()])

    def get_object_admin_url(self, obj) -> str:
        # the url to the Django admin form for the model instance
        info = (obj._meta.app_label, obj._meta.model_name)
        return reverse("admin:{}_{}_change".format(*info), args=(obj.pk,))

    def get_object_full_admin_url(self, obj) -> str:
        return self.url + self.get_object_admin_url(obj)

    def get_navbar_links(self, show_types: list) -> QuerySet[NavbarLink]:
        return self.navbarlink_set.filter(show_type__in=show_types).distinct()

    def get_footer_items(self, show_types: list) -> QuerySet[FooterItem]:
        return self.footeritem_set.filter(
            show_type__in=show_types, footerlink__isnull=False
        ).distinct()

    def get_footer_links(self, show_types: list) -> QuerySet[FooterLink]:
        return self.footerlink_set.filter(
            show_type__in=show_types, footer_item=None
        ).distinct()

    def get_social_media_links(self, show_types: list) -> QuerySet[SocialMediaLink]:
        return self.socialmedialink_set.filter(show_type__in=show_types).distinct()

    class Meta(Model.Meta):
        verbose_name = _("site")
        verbose_name_plural = _("sites")


def clear_site_cache(sender, **kwargs):
    """
    Clear the cache (if primed) each time a site is saved or deleted.
    """
    instance = kwargs["instance"]
    using = kwargs["using"]

    try:
        del SITE_CACHE[instance.pk]
    except KeyError:
        pass
    try:
        del SITE_CACHE[Site.objects.using(using).get(pk=instance.pk)]
    except (KeyError, Site.DoesNotExist):
        pass


pre_save.connect(clear_site_cache, sender=Site)
pre_delete.connect(clear_site_cache, sender=Site)
