from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from one.base.utils.actions import translate_fields
from one.base.utils.admin import FORMFIELD_OVERRIDES_DICT

from .models import Product, ProductFile, ProductImage


@admin.register(ProductFile)
@admin.register(ProductImage)
class ProductFileAdmin(admin.ModelAdmin):
    list_display = ("name", "file")


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    readonly_fields = ("name",)
    actions = [translate_fields]
