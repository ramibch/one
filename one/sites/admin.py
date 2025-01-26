from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from one.base.utils.actions import translate_fields
from one.base.utils.admin import FORMFIELD_OVERRIDES_DICT

from ..articles.tasks import sync_articles
from ..pages.tasks import sync_pages
from .models import Site


@admin.register(Site)
class SiteAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("domain", "brand_name", "picocss_color", "remarks")
    readonly_fields = ("domain",)
    actions = ["sync_articles", "sync_pages", translate_fields]
    fieldsets = (
        (
            _("Site fields"),
            {"fields": ("domain",)},
        ),
        (
            _("Submodules"),
            {"fields": ("article_folders", "page_folders", "books")},
        ),
        (
            _("Brand and design"),
            {
                "fields": (
                    "brand_name",
                    "emoji",
                    "emoji_in_brand",
                    "picocss_color",
                    "footer_links_separator",
                    "change_theme_light_in_navbar",
                    "change_language_in_navbar",
                    "change_theme_light_in_footer",
                    "change_language_in_footer",
                )
            },
        ),
        (
            _("Management"),
            {
                "fields": (
                    "remarks",
                    "default_language",
                    "rest_languages",
                    "requests_duration",
                    "spam_requests_duration",
                )
            },
        ),
        (
            _("SEO"),
            {
                "fields": (
                    "page_title",
                    "page_description",
                    "page_keywords",
                )
            },
        ),
    )

    @admin.action(description="🔄 Sync articles")
    def sync_articles(modeladmin, request, queryset):
        sync_articles(queryset)

    @admin.action(description="🔄 Sync pages")
    def sync_pages(modeladmin, request, queryset):
        sync_pages(queryset)
