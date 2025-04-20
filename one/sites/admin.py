from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from one.base.utils.admin import TranslatableModelAdmin

from ..articles.tasks import sync_articles
from .models import Site


@admin.register(Site)
class SiteAdmin(TranslatableModelAdmin):
    list_display = ("domain", "brand_name", "picocss_color", "remarks")
    # readonly_fields = ("domain",)
    actions = ["sync_articles", "translate_fields"]
    fieldsets = (
        (
            _("Site fields"),
            {"fields": ("domain",)},
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
                    "site_type",
                    "language",
                    "languages",
                    "topics",
                    "requests_duration",
                    "spam_requests_duration",
                    "brand_email_sender",
                    "noreply_email_sender",
                    "remarks",
                )
            },
        ),
        (
            _("SEO"),
            {
                "fields": (
                    "title",
                    "description",
                    "keywords",
                )
            },
        ),
    )

    @admin.action(description="🔄 Sync articles")
    def sync_articles(modeladmin, request, queryset):
        sync_articles(queryset)
