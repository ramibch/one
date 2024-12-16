import contextlib
import string

from auto_prefetch import ForeignKey, Manager, Model
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ManyToManyField, QuerySet
from django.db.models.signals import pre_delete, pre_save
from django.http.request import split_domain_port
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from codebase.articles.models import Article, ArticleParentFolder
from codebase.pages.models import PageParentFolder

from ..base.utils.abstracts import TranslatableModel
from ..menus.models import FooterItem, FooterLink, NavbarLink, SocialMediaLink

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
                SITE_CACHE[host] = self.get(host__name__iexact=host)
            return SITE_CACHE[host]
        except Site.DoesNotExist:
            # Fallback to looking up site after stripping port from the host.
            domain, port = split_domain_port(host)
            if domain not in SITE_CACHE:
                SITE_CACHE[domain] = self.get(host__name__iexact=domain)
            return SITE_CACHE[domain]

    def get_current(self, request):
        return self._get_site_by_request(request)

    def clear_cache(self):
        """Clear the ``Site`` object cache."""
        global SITE_CACHE
        SITE_CACHE = {}


class Site(TranslatableModel):
    PICOCSS = (
        ("amber", _("Amber")),
        ("blue", _("Blue")),
        ("fuchsia", _("Fuchsia")),
        ("jade", _("Jade")),
        ("grey", _("Grey")),
        ("purple", _("Purple")),
        ("cyan", _("Cyan")),
        ("red", _("Read")),
        ("violet", _("Violet")),
        ("indigo", _("Indigo")),
        ("slate", _("Slate")),
        ("lime", _("Lime")),
        ("colors", _("Colors")),
        ("orange", _("Orange")),
        ("pumpkin", _("Pumpkin")),
        ("zinc", _("Zinc")),
        ("sand", _("Sand")),
        ("yellow", _("Yellow")),
        ("pink", _("Pink")),
        ("green", _("Green")),
    )
    name = models.CharField(_("display name"), max_length=50, unique=True)
    remarks = models.TextField(null=True, blank=True)

    emoji = models.CharField(max_length=8, null=True)
    emoji_in_brand = models.BooleanField(default=True)
    page_title = models.CharField(max_length=64, null=True)
    page_description = models.TextField(max_length=256, null=True)
    page_keywords = models.TextField(max_length=128, null=True)

    picocss_color = models.CharField(max_length=16, choices=PICOCSS, default="orange")
    footer_links_separator = models.CharField(max_length=4, default="|")

    change_theme_light_in_footer = models.BooleanField(default=True)
    change_theme_light_in_navbar = models.BooleanField(default=True)
    change_language_in_navbar = models.BooleanField(default=True)
    change_language_in_footer = models.BooleanField(default=True)

    # Management
    last_huey_flush: models.DateTimeField = models.DateTimeField(null=True)
    has_user_home = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    default_language = ForeignKey(
        "base.Language",
        default=settings.LANGUAGE_CODE,
        on_delete=models.SET_DEFAULT,
        verbose_name=_("Default language"),
        related_name="sites_with_default_languages",
    )
    rest_languages = ManyToManyField(
        "base.Language",
        verbose_name=_("Rest of languages"),
        related_name="sites_with_rest_languages",
    )

    # Submodules
    article_folders = ManyToManyField("articles.ArticleParentFolder")
    page_folders = ManyToManyField("pages.PageParentFolder")

    def __str__(self):
        return self.name

    @cached_property
    def main_domain(self):
        return self.domain_set.filter(is_main=True).first()

    @cached_property
    def languages(self):
        from ..base.models import Language

        qs1 = self.rest_languages.all()
        qs2 = Language.objects.filter(id=self.default_language_id)
        return (qs1 | qs2).distinct()

    @cached_property
    def languages_count(self) -> int:
        return self.languages.count()

    def get_default_language(self):
        return self.default_language

    def get_rest_languages(self):
        return self.rest_languages

    @cached_property
    def articles(self):
        return Article.objects.filter(
            submodule_folder__in=self.article_folders.all()
        ).distinct()

    @cached_property
    def picocss_static_url(self) -> str:
        return f"{settings.STATIC_URL}css/picocss/pico.{self.picocss_color}.min.css"

    def get_attr_name_for_submodule_model(self, Model) -> str:
        if Model == ArticleParentFolder:
            return "article_folders"
        if Model == PageParentFolder:
            return "page_folders"
        raise TypeError(f"The model {Model} is not recognised in the application.")

    def get_submodule_folders(self, Model, sites_filter=True):
        attr_name = self.get_attr_name_for_submodule_model(Model)
        submodule_folder_attr = getattr(self, attr_name)
        if sites_filter:
            return submodule_folder_attr.filter(sites__in=[self])
        return submodule_folder_attr.all()

    def get_submodule_folders_as_list(self, Model):
        objs = self.get_submodule_folders(Model)
        return [f.name for f in objs] if objs else []

    @cached_property
    def url(self) -> str:
        schema = "https" if settings.HTTPS else "http"
        return f"{schema}://{self.main_domain}"

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

    objects = SiteManager()

    class Meta(TranslatableModel.Meta):
        verbose_name = _("site")
        verbose_name_plural = _("sites")
        ordering = ["host__name"]


class Host(Model):
    site = ForeignKey("sites.Site", on_delete=models.CASCADE)
    name = models.CharField(
        _("domain name"),
        max_length=100,
        validators=[_simple_domain_name_validator],
        primary_key=True,
    )
    is_main = models.BooleanField(default=True)

    def __str__(self):
        return self.name


def clear_site_cache(sender, **kwargs):
    """
    Clear the cache (if primed) each time a site is saved or deleted.
    """
    instance = kwargs["instance"]
    using = kwargs["using"]
    with contextlib.suppress(KeyError):
        del SITE_CACHE[instance.pk]
    with contextlib.suppress(KeyError, Site.DoesNotExist):
        del SITE_CACHE[Site.objects.using(using).get(pk=instance.pk).main_domain]


pre_save.connect(clear_site_cache, sender=Site)
pre_delete.connect(clear_site_cache, sender=Site)
