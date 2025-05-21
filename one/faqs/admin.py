from django.contrib import admin

from one.admin import TranslatableModelAdmin

from .models import FAQ, FAQCategory


@admin.register(FAQ)
class FAQAdmin(TranslatableModelAdmin):
    list_display = ("question", "answer")
    search_fields = ("question", "answer")


@admin.register(FAQCategory)
class FAQCategoryAdmin(TranslatableModelAdmin):
    pass
