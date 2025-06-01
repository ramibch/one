from django.contrib import admin

from one.admin import OneTranslatableModelAdmin

from .models import FAQ, FAQCategory


@admin.register(FAQ)
class FAQAdmin(OneTranslatableModelAdmin):
    list_display = ("question", "answer")
    search_fields = ("question", "answer")


@admin.register(FAQCategory)
class FAQCategoryAdmin(OneTranslatableModelAdmin):
    pass
