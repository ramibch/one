from django.contrib import admin

from one.base.utils.admin import TranslatableModelAdmin

from .models import Link


@admin.register(Link)
class LinkAdmin(TranslatableModelAdmin):
    list_display = ("__str__", "django_url_path", "plan", "article")
    list_editable = ("django_url_path", "plan", "article")
    search_fields = ("article", "plan")
    autocomplete_fields = ("article", "plan")
