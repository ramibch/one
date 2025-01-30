from django.contrib import admin, messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from one.base.utils.actions import translate_fields
from one.base.utils.admin import FORMFIELD_OVERRIDES_DICT
from one.products.models import Product

from .models import App, Listing, Shop


@admin.register(Shop)
class ShopAdmin(TranslationAdmin):
    list_display = ("__str__",)
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    actions = [translate_fields, "generate_listings"]

    @admin.action(description="🚀 Create listings from products using topics")
    def generate_listings(modeladmin, request, queryset):
        listings = []
        for shop in queryset:
            products = Product.objects.filter(topics__in=shop.topics.all())
            for product in products:
                if Listing.objects.filter(product=product, shop=shop).exists():
                    continue
                listings.append(
                    Listing(
                        product=product,
                        shop=shop,
                        price=shop.price_percentage / 100 * product.price,
                    )
                )
        Listing.objects.bulk_create(listings)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "price", "url")
    readonly_fields = ("listing_id", "url", "state")
    actions = ["upload"]

    @admin.action(description="⬆️ Upload to Etsy")
    def upload(modeladmin, request, queryset):
        for obj in queryset.filter(listing_id__isnull=True):
            obj.upload_to_etsy()


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    readonly_fields = (
        "access_token",
        "refresh_token",
        "expires_at",
        "code_verifier",
        "state",
        "code",
    )
    list_display = ("name", "keystring", "expires_at")
    actions = ["request_auth"]

    @admin.action(description="👤 Request Etsy auth")
    def request_auth(modeladmin, request, queryset):
        if queryset.count() == 1:
            return redirect(queryset.first().request_auth_url)
        messages.error(request, _("Select just one object"))
