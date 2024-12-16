from modeltranslation.translator import TranslationOptions, register

from .models import ExampleModel


@register(ExampleModel)
class ExampleModelOptions(TranslationOptions):
    fields = ()
