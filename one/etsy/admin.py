from django.contrib import admin, messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from one.base.utils.actions import translate_fields
from one.base.utils.admin import FORMFIELD_OVERRIDES_DICT

from .models import App, ProductListing, Shop, UserListing, UserShop, UserShopAuth
from .tasks import task_generate_listings_from_products, task_upload_listings


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("name", "keystring", "redirect_uri", "scopes")
    actions = ["request_auth"]

    @admin.action(description="👤 Request Etsy auth")
    def request_auth(modeladmin, request, queryset):
        if queryset.count() == 1:
            return redirect(queryset.first().request_auth_url)
        messages.error(request, _("Select just one object"))


@admin.register(Shop)
class ShopAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("__str__", "price_percentage")
    readonly_fields = ("etsy_payload",)
    actions = [translate_fields, "generate_listings", "get_payload"]

    @admin.action(description="🚀 Create listings from products using topics")
    def generate_listings(modeladmin, request, queryset):
        task_generate_listings_from_products(queryset)

    @admin.action(description="🛍️ Request Etsy payload")
    def get_payload(modeladmin, request, queryset):
        for shop in queryset:
            shop.request_and_save_payload()


@admin.register(ProductListing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "price", "url")
    readonly_fields = ("listing_id", "url", "state", "response")
    actions = ["upload"]

    @admin.action(description="⬆️ Upload to Etsy")
    def upload(modeladmin, request, queryset):
        task_upload_listings(queryset.filter(listing_id__isnull=True))


@admin.register(UserShopAuth)
class UserShopAuthAdmin(admin.ModelAdmin):
    list_display = ("__str__", "etsy_user_id", "shop_id", "app", "user", "expires_at")
    readonly_fields = [f.name for f in UserShopAuth._meta.fields]
    actions = ["refresh"]

    def has_add_permission(self, request):
        return False

    @admin.action(description="🔄 Refresh token")
    def refresh(modeladmin, request, queryset):
        for obj in queryset:
            api = obj.get_api_client()
            api.refresh()


@admin.register(UserShop)
class UserShopAdmin(admin.ModelAdmin):
    list_display = ("name", "user_shop_auth")



@admin.register(UserListing)
class UserListingAdmin(admin.ModelAdmin):
    readonly_fields = (
        "state",
        "creation_timestamp",
        "created_timestamp",
        "ending_timestamp",
        "original_creation_timestamp",
        "last_modified_timestamp",
        "updated_timestamp",
        "state_timestamp",
        "featured_rank",
        "url",
        "num_favorers",
        "non_taxable",
        "is_private",
        "language",
        "state",
        "creation_timestamp",
        "created_timestamp",
        "ending_timestamp",
        "original_creation_timestamp",
        "last_modified_timestamp",
        "updated_timestamp",
        "state_timestamp",
        "featured_rank",
        "url",
        "num_favorers",
        "non_taxable",
        "is_private",
        "language",
    )
