from django.contrib import admin

from one.admin import OneTranslatableModelAdmin

from .models import Link


@admin.register(Link)
class LinkAdmin(OneTranslatableModelAdmin):
    list_display = ("__str__", "url_path", "topic", "external_url")
    list_editable = ("url_path", "topic", "external_url")
    search_fields = ("topic", "url_path", "external_url")
