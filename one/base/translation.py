from modeltranslation.translator import TranslationOptions, register

from .models import Topic


@register(Topic)
class TopicOptions(TranslationOptions):
    fields = ("name", "slug")
