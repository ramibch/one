from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from one.base.utils.actions import translation_actions
from one.base.utils.admin import FORMFIELD_OVERRIDES_DICT

from ..articles.tasks import sync_articles
from ..pages.tasks import sync_pages
from .models import Host, Seo, Site


class HostInline(admin.TabularInline):
    model = Host
    extra = 0


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ("name", "site", "is_main")


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("name", "brand_name", "picocss_color", "remarks")
    readonly_fields = ("name",)
    actions = ["sync_articles", "sync_pages"]
    inlines = (HostInline,)
    fieldsets = (
        (
            _("Site fields"),
            {"fields": ("name",)},
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
    )

    @admin.action(description="🔄 Sync articles")
    def sync_articles(modeladmin, request, queryset):
        sync_articles(queryset)

    @admin.action(description="🔄 Sync pages")
    def sync_pages(modeladmin, request, queryset):
        sync_pages(queryset)


@admin.register(Seo)
class SeoAdmin(TranslationAdmin):
    list_display = ("page_title", "page_description", "page_keywords")
    actions = translation_actions
