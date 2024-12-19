from django.contrib import admin, messages
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from huey.contrib.djhuey import HUEY
from modeltranslation.admin import TranslationAdmin

from codebase.base.utils.actions import translation_actions
from codebase.base.utils.admin import FORMFIELD_OVERRIDES_DICT

from ..articles.tasks import trigger_sync_articles
from ..menus.models import create_initial_menu_objects
from ..pages.tasks import trigger_sync_pages
from .models import Host, Site


class DomainInline(admin.TabularInline):
    model = Host
    extra = 0


@admin.register(Site)
class SiteAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT  # type: ignore
    list_display = ("__str__", "name")
    search_fields = ("host__name", "name")
    readonly_fields = ("last_huey_flush",)
    list_editable = ("name",)
    actions = translation_actions + [
        "flush_huey",
        "sync_articles",
        "sync_pages",
        "create_menus",
    ]
    inlines = (DomainInline,)

    fieldsets = (
        (
            _("Site fields"),
            {"fields": ("name",)},
        ),
        (
            _("Management"),
            {
                "fields": (
                    "remarks",
                    "last_huey_flush",
                    "allow_translation",
                    "override_translated_fields",
                    "default_language",
                    "rest_languages",
                )
            },
        ),
        (
            _("Submodules"),
            {"fields": ("article_folders", "page_folders", "books")},
        ),
        (
            _("Brand"),
            {"fields": ("emoji", "emoji_in_brand")},
        ),
        (
            _("Defaults"),
            {"fields": ("page_title", "page_description", "page_keywords")},
        ),
        (
            _("Appearance and design"),
            {
                "fields": (
                    "picocss_color",
                    "footer_links_separator",
                    "change_theme_light_in_navbar",
                    "change_language_in_navbar",
                    "change_theme_light_in_footer",
                    "change_language_in_footer",
                )
            },
        ),
    )

    @admin.action(description="🗑️ Flush Huey | revoke tasks")
    def flush_huey(modeladmin, request, queryset):
        HUEY.flush()
        queryset.update(last_huey_flush=now())

    @admin.action(description="🔄 Sync articles")
    def sync_articles(modeladmin, request, queryset):
        trigger_sync_articles(queryset)

    @admin.action(description="🔄 Sync pages")
    def sync_pages(modeladmin, request, queryset):
        trigger_sync_pages(queryset)

    @admin.action(description="☰ Create initial menus")
    def create_menus(modeladmin, request, queryset):
        created = create_initial_menu_objects(queryset)
        if created:
            messages.info(request, _("Menus objects were created!"))
        else:
            messages.warning(
                request,
                _("Not created! Check menu objects associated with the selected sites"),
            )
