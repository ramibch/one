from django.contrib import admin, messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from one.base.utils.actions import translate_fields
from one.base.utils.admin import FORMFIELD_OVERRIDES_DICT

from .models import App, Listing, Shop, UserShopAuth
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
    list_display = ("__str__", "price_percentage")
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    actions = [translate_fields, "generate_listings"]

    @admin.action(description="🚀 Create listings from products using topics")
    def generate_listings(modeladmin, request, queryset):
        task_generate_listings_from_products(queryset)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "price", "url")
    readonly_fields = ("listing_id", "url", "state", "response")
    actions = ["upload"]

    @admin.action(description="⬆️ Upload to Etsy")
    def upload(modeladmin, request, queryset):
        task_upload_listings(queryset.filter(listing_id__isnull=True))


@admin.register(UserShopAuth)
class UserShopAuthAdmin(admin.ModelAdmin):
    readonly_fields = [f.name for f in UserShopAuth._meta.fields]

    def has_add_permission(self, request):
        return False
