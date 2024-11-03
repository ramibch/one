from django.contrib import admin

from .models import FooterItem, FooterLink, NavbarLink, SocialMediaLink


@admin.action(description="0️⃣ Set order 0")
def set_order_0(modeladmin, request, queryset):
    queryset.update(order=0)


@admin.action(description="1️⃣ Set order 1")
def set_order_1(modeladmin, request, queryset):
    queryset.update(order=1)


@admin.action(description="2️⃣ Set order 2")
def set_order_2(modeladmin, request, queryset):
    queryset.update(order=2)


@admin.action(description="3️⃣ Set order 3")
def set_order_3(modeladmin, request, queryset):
    queryset.update(order=3)


@admin.action(description="4️⃣ Set order 4")
def set_order_4(modeladmin, request, queryset):
    queryset.update(order=4)


@admin.action(description="5️⃣ Set order 5")
def set_order_5(modeladmin, request, queryset):
    queryset.update(order=5)


@admin.action(description="👁️ Show always")
def show_always(modeladmin, request, queryset):
    queryset.update(show_type="always")


@admin.action(description="🫣 Never show")
def never_show(modeladmin, request, queryset):
    queryset.update(show_type="never")


@admin.action(description="👤 Show when user is logged in")
def show_for_logged_user(modeladmin, request, queryset):
    queryset.update(show_type="user")


@admin.action(description="🕵🏻 Show for anonymous user")
def show_for_anonymous_user(modeladmin, request, queryset):
    queryset.update(show_type="no_user")


@admin.action(description="🔗 Show link as emoji")
def show_as_emoji(modeladmin, request, queryset):
    queryset.filter(emoji=None).update(emoji="🔗")
    queryset.update(show_as_emoji=True)


@admin.action(description="🙅‍♂️ Do not show as emoji")
def dont_show_as_emoji(modeladmin, request, queryset):
    queryset.update(show_as_emoji=True)


@admin.action(description="✅ Set new tab")
def set_new_tab(modeladmin, request, queryset):
    queryset.update(new_tab=True)


@admin.action(description="❌ No new tab")
def set_no_new_tab(modeladmin, request, queryset):
    queryset.update(new_tab=False)


ORDER_ACTIONS = [set_order_0, set_order_1, set_order_2, set_order_3, set_order_4, set_order_5]

SHOW_ACTIONS = [show_always, never_show, show_for_logged_user, show_for_anonymous_user]

SHOW_AS_EMOJI_ACTIONS = [show_as_emoji, dont_show_as_emoji]

NEW_TAB_ACTIONS = [set_new_tab, set_no_new_tab]


@admin.register(NavbarLink)
class NavbarLinkAdmin(admin.ModelAdmin):
    list_display = ("display_title", "show_type", "show_as_emoji", "new_tab", "order")
    list_filter = ("show_type", "show_as_emoji", "new_tab", "order")
    actions = ORDER_ACTIONS + SHOW_ACTIONS + NEW_TAB_ACTIONS + SHOW_AS_EMOJI_ACTIONS


class FooterLinkInline(admin.StackedInline):
    model = FooterLink
    extra = 1


@admin.register(FooterItem)
class FooterItemAdmin(admin.ModelAdmin):
    list_display = ("title", "display_title", "show_type", "order")
    list_filter = ("show_type", "order")
    actions = ORDER_ACTIONS + SHOW_ACTIONS
    inlines = (FooterLinkInline,)


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ("display_title", "footer_item", "show_type", "order")
    list_filter = ("show_type", "order", "new_tab", "footer_item")
    actions = ORDER_ACTIONS + SHOW_ACTIONS + NEW_TAB_ACTIONS


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "new_tab", "show_type", "order")
    list_filter = ("show_type", "new_tab", "order")
    actions = ORDER_ACTIONS + SHOW_ACTIONS + NEW_TAB_ACTIONS
