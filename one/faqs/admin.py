from django.contrib import admin

from one.base.utils.admin import TranslatableModelAdmin

from .models import FAQ


@admin.register(FAQ)
class FAQAdmin(TranslatableModelAdmin):
    list_display = ("question", "answer", "category")
    list_editable = ("category",)
    search_fields = ("question", "answer")
