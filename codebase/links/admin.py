from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Link


@admin.register(Link)
class LinkAdmin(TranslationAdmin):
    pass
