from django.contrib import admin

from one.base.utils.admin import TranslatableModelAdmin

from .models import EtsyListing, EtsyShop, Product, ProductFile, ProductImage
from .tasks import task_generate_listings_from_products, task_upload_listings


@admin.register(ProductFile)
@admin.register(ProductImage)
class ProductFileAdmin(admin.ModelAdmin):
    list_display = ("name", "file")


@admin.register(Product)
class ProductAdmin(TranslatableModelAdmin):
    readonly_fields = ("name",)


@admin.register(EtsyListing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "price", "url")
    readonly_fields = ("listing_id", "url", "state", "response")
    actions = ["upload"]

    @admin.action(description="⬆️ Upload to Etsy")
    def upload(modeladmin, request, queryset):
        task_upload_listings(queryset.filter(listing_id__isnull=True))


@admin.register(EtsyShop)
class ShopAdmin(TranslatableModelAdmin):
    list_display = ("__str__", "price_percentage")
    readonly_fields = ("etsy_payload",)
    actions = ["generate_listings", "get_payload", "translate_fields"]

    @admin.action(description="🚀 Create listings from products using topics")
    def generate_listings(modeladmin, request, queryset):
        task_generate_listings_from_products(queryset)

    @admin.action(description="🛍️ Request Etsy payload")
    def get_payload(modeladmin, request, queryset):
        for shop in queryset:
            shop.request_and_save_payload()
