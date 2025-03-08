from django import forms
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import FieldDoesNotExist

from .telegram import Bot


def update_model_from_dict(db_obj, data_dict, save: bool = True):
    """
    Updates a model object from a dictionary
    db_obj.<key> = value <-> dict[key, value]

    """
    model_class = db_obj.__class__

    for key, value in data_dict.items():
        try:
            field = model_class._meta.get_field(key)

            # Skip updating auto fields like primary keys
            if field.auto_created or field.primary_key or field.is_relation:
                continue

            setattr(db_obj, key, value)

        except FieldDoesNotExist:
            # Ignore fields that don't exist in the model
            pass
        except Exception as e:
            Bot.to_admin(f"Error setting {key}: {e}\n{model_class}\n{db_obj.pk}")

    if save:
        db_obj.save()

    return db_obj


class ChoiceArrayField(ArrayField):
    """
    # https://gist.github.com/danni/f55c4ce19598b2b345ef

    A field that allows us to store an array of choices.

    Uses Django 1.9's postgres ArrayField
    and a MultipleChoiceField for its formfield.

    Usage:

        choices = ChoiceArrayField(models.CharField(max_length=...,
                                                    choices=(...,)),
                                   default=[...])
    """

    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "choices": self.base_field.choices,
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't
        # care for it.
        # pylint:disable=bad-super-call
        return super(ArrayField, self).formfield(**defaults)
