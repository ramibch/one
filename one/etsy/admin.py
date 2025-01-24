from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from one.base.utils.actions import translation_actions

from .models import Listing, Shop


@admin.register(Shop)
class ShopAdmin(TranslationAdmin):
    actions = translation_actions


@admin.register(Listing)
class ListingAdmin(TranslationAdmin):
    actions = translation_actions
