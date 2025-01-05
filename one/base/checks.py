from django.core.checks import Error

from .utils.abstracts import TranslatableModel


def check_abstract_models(*, app_configs, databases, **kwargs):
    errors = []

    for model_class in TranslatableModel.__subclasses__():
        if model_class.get_default_language is None:  # pragma: no cover
            errors.append(
                Error(
                    "get_default_language not present",
                    hint=f"Add a method `get_default_language` to {model_class}",
                    obj=model_class,
                    id="TranslatableModel.E001",
                )
            )
        if model_class.get_rest_languages is None:  # pragma: no cover
            errors.append(
                Error(
                    "get_rest_languages not present",
                    hint=f"Add a method `get_rest_languages` to {model_class}",
                    obj=model_class,
                    id="TranslatableModel.E002",
                )
            )

    return errors
