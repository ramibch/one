from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Link


@admin.register(Link)
class LinkAdmin(TranslationAdmin):
    list_display = ("__str__", "django_url_path", "page", "plan", "article")
    list_editable = ("django_url_path", "page", "plan", "article")
    search_fields = ("article", "page", "plan")
    autocomplete_fields = ("article", "page", "plan")
