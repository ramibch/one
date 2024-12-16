from django.core.checks import Error

from .utils.abstracts import BasePageFileModel, BasePageModel, TranslatableModel


def check_abstract_models(*, app_configs, databases, **kwargs):
    errors = []

    for model_class in TranslatableModel.__subclasses__():
        if model_class.get_default_language is None:
            errors.append(
                Error(
                    "get_default_language not present",
                    hint=f"Add a method `get_default_language` to {model_class}",
                    obj=model_class,
                    id="TranslatableModel.E001",
                )
            )
        if model_class.get_rest_languages is None:
            errors.append(
                Error(
                    "get_rest_languages not present",
                    hint=f"Add a method `get_rest_languages` to {model_class}",
                    obj=model_class,
                    id="TranslatableModel.E002",
                )
            )

    for model_class in BasePageModel.__subclasses__():
        if model_class.parent is None:
            errors.append(
                Error(
                    "parent not present",
                    hint=f"Add a field `parent` to {model_class}",
                    obj=model_class,
                    id="BasePageModel.E001",
                )
            )
    for model_class in BasePageFileModel.__subclasses__():
        if model_class.parent is None:
            errors.append(
                Error(
                    "parent not present",
                    hint=f"Add a field `parent` to {model_class}",
                    obj=model_class,
                    id="PageFileModel.E001",
                )
            )
    return errors
