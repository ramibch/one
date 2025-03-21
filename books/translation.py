from modeltranslation.translator import TranslationOptions, register

from .models import Chapter


@register(Chapter)
class ChapterOptions(TranslationOptions):
    fields = ("title", "body", "slug")
