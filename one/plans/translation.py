from modeltranslation.translator import TranslationOptions, register

from .models import Plan


@register(Plan)
class PlanOptions(TranslationOptions):
    fields = ("title", "description")
