import subprocess
from copy import copy
from itertools import chain
from statistics import mode

from auto_prefetch import Model
from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from django.utils.text import slugify

from .exceptions import SubmoduleException


class BaseSubmoduleFolder(Model):
    name = models.CharField(max_length=64, unique=True)
    present_in_filesystem = models.BooleanField(default=True)

    def __init_subclass__(cls, submodule, **kwargs):
        cls.submodule = submodule
        cls.submodule_path = settings.SUBMODULES_PATH / submodule
        super().__init_subclass__(**kwargs)

    class Meta(Model.Meta):
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
                raise SubmoduleException(f"{cls.submodule_path} is not a directory")
            objs = []
            folder_names = [p.name for p in cls.submodule_path.iterdir() if p.is_dir()]
            for folder_name in folder_names:
                objs.append(cls._meta.model(name=folder_name))
            cls.objects.bulk_create(
                objs,
                update_fields=["name"],
                unique_fields=["name"],
                update_conflicts=True,
            )


class TranslatableModel(Model):
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
        langs.remove(self.get_default_language())
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
