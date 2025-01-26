from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from one.base.utils.actions import translate_fields
from one.base.utils.admin import FORMFIELD_OVERRIDES_DICT
from one.products.models import Product

from .models import Listing, Shop


@admin.register(Shop)
class ShopAdmin(TranslationAdmin):
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
                        price=shop.overprice_percentage / 100 * product.price,
                    )
                )
        Listing.objects.bulk_create(listings)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    pass
