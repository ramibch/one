from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from one.base.utils.actions import translate_fields
from one.base.utils.admin import FORMFIELD_OVERRIDES_DICT

from .models import EtsyListing, EtsyShop, Product, ProductFile, ProductImage
from .tasks import task_generate_listings_from_products, task_upload_listings


@admin.register(ProductFile)
@admin.register(ProductImage)
class ProductFileAdmin(admin.ModelAdmin):
    list_display = ("name", "file")


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    readonly_fields = ("name",)
    actions = [translate_fields]


@admin.register(EtsyListing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "price", "url")
    readonly_fields = ("listing_id", "url", "state", "response")
    actions = ["upload"]

    @admin.action(description="⬆️ Upload to Etsy")
    def upload(modeladmin, request, queryset):
        task_upload_listings(queryset.filter(listing_id__isnull=True))


@admin.register(EtsyShop)
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
