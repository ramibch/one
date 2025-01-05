from modeltranslation.translator import TranslationOptions, register

from .models import Article


@register(Article)
class ArticleOptions(TranslationOptions):
    fields = ("title", "body", "slug")
