import subprocess
from copy import copy
from itertools import chain
from statistics import mode

from auto_prefetch import Model
from django import forms
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from one.bot import Bot

# Proejct models


class OneModel(Model):
    # TODO: Add these fields!
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    @cached_property
    def admin_url(self) -> str:
        return reverse(
            f"admin:{self._meta.app_label}_{self._meta.model_name}_change",
            args=(self.pk,),
        )

    @cached_property
    def full_admin_url(self) -> str:
        return settings.MAIN_WEBSITE_URL + self.admin_url

    class Meta(Model.Meta):
        abstract = True


class BaseSubmoduleFolder(OneModel):
    name = models.CharField(max_length=64, unique=True, editable=False, db_index=True)
    present_in_filesystem = models.BooleanField(default=True, editable=False)

    def __init_subclass__(cls, submodule, **kwargs):
        cls.submodule = submodule
        cls.submodule_path = settings.SUBMODULES_PATH / submodule
        super().__init_subclass__(**kwargs)

    class Meta(OneModel.Meta):
        abstract = True

    def __str__(self):
        return self.name

    @cached_property
    def folder_path(self):
        return self.submodule_path / self.name

    @staticmethod
    def fetch_submodules():
        subprocess.call(["git", "submodule", "update", "--remote"])

    @classmethod
    def sync_folders(cls, fetch=True):
        if fetch:
            cls.fetch_submodules()

        if cls == BaseSubmoduleFolder:
            for Submodule in cls.__subclasses__():
                Submodule.sync_folders(fetch=False)
        else:
            if not cls.submodule_path.is_dir():
                raise OSError(f"{cls.submodule_path} is not a directory")

            ModelClass = cls._meta.model
            dir_names = [p.name for p in cls.submodule_path.iterdir() if p.is_dir()]
            objs = [ModelClass(name=dn) for dn in dir_names if not dn.startswith("_")]
            cls.objects.bulk_create(
                objs,
                update_fields=["name"],
                unique_fields=["name"],
                update_conflicts=True,
            )


class TranslatableModel(OneModel):
    LANG_ATTR = None
    LANGS_ATTR = None
    I18N_SLUGIFY_FROM = None

    @cached_property
    def language_count(self):
        return len(self.get_languages())

    def get_default_language(self):
        if self.LANG_ATTR is None:
            raise ValueError("LANG_ATTR not defined in model.")

        langs = list(
            set(
                self.__class__.objects.filter(pk=self.pk).values_list(
                    self.LANG_ATTR, flat=True
                )
            )
        )

        if len(langs) == 0 or settings.LANGUAGE_CODE in langs:
            return settings.LANGUAGE_CODE
        elif len(langs) == 1:
            return langs[0]
        else:
            return mode(langs)

    def get_languages(self):
        if self.LANGS_ATTR is None:
            raise ValueError("LANGS_ATTR not defined in model.")

        if self.pk is None:
            raise ValueError("No Primary Key set.")

        lists_of_langs = self.__class__.objects.filter(pk=self.pk).values_list(
            self.LANGS_ATTR, flat=True
        )
        flattened_list = chain.from_iterable(lists_of_langs)

        return list(dict.fromkeys(flattened_list))

    def get_languages_without_default(self):
        langs = copy(self.get_languages())
        try:
            langs.remove(self.get_default_language())
        except ValueError:
            pass
        return langs

    def save(self, *args, **kwargs):
        if self.I18N_SLUGIFY_FROM:
            if not hasattr(self, "slug"):
                raise AttributeError("Model has no 'slug' attribute.")

            for lang in settings.LANGUAGE_CODES:
                value = getattr(self, f"{self.I18N_SLUGIFY_FROM}_{lang}", None)
                if value:
                    setattr(self, f"slug_{lang}", slugify(value))

        super().save(*args, **kwargs)

    class Meta(Model.Meta):
        abstract = True


# Functions


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


def get_db_session_object(request):
    try:
        session_key = request.session.session_key
        db_session = Session.objects.get(pk=session_key)
    except (KeyError, Session.DoesNotExist):
        session_store = SessionStore()
        session_store.create()
        session_key = session_store.session_key
        request.session["sessionid"] = session_key
        db_session = Session.objects.get(session_key=session_key)
    return db_session


# Fields


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


# Choices


class Genders(models.TextChoices):
    MALE = "m", _("male")
    FEMALE = "f", _("female")
