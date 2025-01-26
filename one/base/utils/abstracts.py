import subprocess

from auto_prefetch import Model
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from one.base import Languages
from one.base.utils.db_fields import ChoiceArrayField

from .exceptions import SubmoduleException


class BaseSubmoduleFolder(Model):
    name = models.CharField(max_length=64, unique=True)

    def __init_subclass__(cls, submodule, **kwargs):
        cls.submodule = submodule
        cls.submodule_path = settings.SUBMODULES_PATH / submodule
        super().__init_subclass__(**kwargs)

    class Meta(Model.Meta):
        abstract = True

    def __str__(self):
        return self.name

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


class SingletonModel(Model):
    """Singleton Django Model"""

    _singleton = models.BooleanField(default=True, editable=False, unique=True)

    class Meta(Model.Meta):
        abstract = True

    @classmethod
    def load(cls):
        return cls.objects.get_or_create()[0]

    @classmethod
    def get(cls):
        return cls.load()


class TranslatableModel(Model):
    default_language = models.CharField(
        max_length=4,
        choices=Languages,
        default=Languages.EN,
    )
    languages = ChoiceArrayField(
        models.CharField(max_length=8, choices=Languages),
        default=list,
        blank=True,
    )

    @cached_property
    def language_count(self):
        return len(self.languages)

    def clean(self):
        super().clean()
        if self.default_language not in self.languages:
            raise ValidationError(_("Default language must be included in languages"))

    class Meta(Model.Meta):
        abstract = True
