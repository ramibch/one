from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from huey.contrib.djhuey import HUEY
from modeltranslation.admin import TranslationAdmin

from codebase.base.utils.actions import translation_actions
from codebase.base.utils.admin import FORMFIELD_OVERRIDES_DICT

from ..articles.tasks import trigger_sync_articles_task
from ..menus.models import create_initial_menu_objects
from ..pages.tasks import trigger_sync_pages_task
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
    actions = ["flush_huey", "sync_articles", "sync_pages", "create_menus"]
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
                    "spammy_requests_duration",
                )
            },
        ),
    )

    @admin.action(description="🗑️ Flush Huey | revoke tasks")
    def flush_huey(modeladmin, request, queryset):
        HUEY.flush()

    @admin.action(description="🔄 Sync articles")
    def sync_articles(modeladmin, request, queryset):
        trigger_sync_articles_task(queryset)

    @admin.action(description="🔄 Sync pages")
    def sync_pages(modeladmin, request, queryset):
        trigger_sync_pages_task(queryset)

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


@admin.register(Seo)
class SeoAdmin(TranslationAdmin):
    list_display = ("page_title", "page_description", "page_keywords")
    actions = translation_actions
