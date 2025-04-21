from django.contrib import admin

from one.base.utils.admin import TranslatableModelAdmin

from .models import Link


@admin.register(Link)
class LinkAdmin(TranslatableModelAdmin):
    list_display = ("__str__", "url_path", "topic", "external_url")
    list_editable = ("url_path", "topic", "external_url")
    search_fields = ("topic", "url_path", "external_url")
