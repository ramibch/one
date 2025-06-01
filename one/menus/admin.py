from django.contrib import admin

from one.admin import OneModelAdmin, OneStackedInline, OneTranslatableModelAdmin

from .models import FooterItem, FooterLink, NavbarLink, SocialMediaLink


@admin.register(NavbarLink)
class NavbarLinkAdmin(OneModelAdmin):
    list_display = (
        "display_title",
        "emoji",
        "show_type",
        "show_as_emoji",
        "new_tab",
        "order",
    )
    list_filter = ("sites", "show_type", "show_as_emoji", "new_tab", "order")
    list_editable = ("show_type", "order", "emoji", "show_as_emoji", "new_tab")


class FooterLinkInline(OneStackedInline):
    model = FooterLink
    extra = 1
    exclude = ("site",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(footer_item__isnull=False)


@admin.register(FooterItem)
class FooterItemAdmin(OneTranslatableModelAdmin):
    list_display = ("display_title", "emoji", "show_type", "order")
    list_editable = ("emoji", "show_type", "order")
    list_filter = ("sites", "show_type", "order")
    inlines = (FooterLinkInline,)


@admin.register(FooterLink)
class FooterLinkAdmin(OneModelAdmin):
    list_display = ("display_title", "footer_item", "show_type", "new_tab", "order")
    list_editable = ("show_type", "footer_item", "new_tab", "order")
    list_filter = ("sites", "show_type", "order", "new_tab", "footer_item")


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(OneModelAdmin):
    list_display = ("platform", "new_tab", "show_type", "order")
    list_editable = ("show_type", "new_tab", "order")
    list_filter = ("sites", "show_type", "new_tab", "order")
