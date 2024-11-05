from django.contrib import admin

from .models import FooterItem, FooterLink, NavbarLink, SocialMediaLink


@admin.register(NavbarLink)
class NavbarLinkAdmin(admin.ModelAdmin):
    list_display = ("display_title", "emoji", "show_type", "show_as_emoji", "new_tab", "order")
    list_filter = ("show_type", "show_as_emoji", "new_tab", "order")
    list_editable = ("show_type", "order", "emoji", "show_as_emoji", "new_tab")


class FooterLinkInline(admin.StackedInline):
    model = FooterLink
    extra = 1


@admin.register(FooterItem)
class FooterItemAdmin(admin.ModelAdmin):
    list_display = ("display_title", "title", "show_type", "order")
    list_editable = ("show_type", "order")
    list_filter = ("show_type", "order")
    inlines = (FooterLinkInline,)


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ("display_title", "footer_item", "show_type", "new_tab", "order")
    list_editable = ("show_type", "footer_item", "new_tab", "order")
    list_filter = ("show_type", "order", "new_tab", "footer_item")


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "new_tab", "show_type", "order")
    list_editable = ("show_type", "new_tab", "order")
    list_filter = ("show_type", "new_tab", "order")
