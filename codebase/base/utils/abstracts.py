import subprocess

from auto_prefetch import Model
from django.conf import settings
from django.db import models

from .exceptions import SubmoduleException
from .mixins import PageMixin


class BaseSubmoduleFolder(Model):
    name = models.CharField(max_length=64, unique=True)
    sites = models.ManyToManyField("sites.Site")

    def __init_subclass__(cls, submodule, **kwargs):
        cls._submodule = submodule
        super().__init_subclass__(**kwargs)

    class Meta(Model.Meta):
        abstract = True

    def __str__(self):
        return self.name

    @staticmethod
    def fetch_submodules():
        subprocess.call(["git", "submodule", "update", "--remote"])

    @classmethod
    def sync_all_folders(cls):
        cls.fetch_submodules()

        if cls == BaseSubmoduleFolder:
            for Submodule in cls.__subclasses__():
                Submodule.sync_folders()
        else:
            print(f"⚠️  Just syncing for '{cls._submodule}'.")
            cls.sync_folders()

    @classmethod
    def sync_folders(cls):
        if cls == BaseSubmoduleFolder:
            cls.sync_all_folders()
            return

        cls.fetch_submodules()

        submodule_path = settings.SUBMODULES_PATH / cls._submodule
        if not submodule_path.is_dir():
            raise SubmoduleException(f"Submodule {submodule_path} is not a directory")

        objs = []
        for folder_name in [p.name for p in submodule_path.iterdir() if p.is_dir()]:
            objs.append(cls._meta.model(name=folder_name))

        cls.objects.bulk_create(
            objs, update_fields=["name"], unique_fields=["name"], update_conflicts=True
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
    get_default_language = None  # Implement in the subclass
    get_rest_languages = None  # Implement in the subclass
    allow_translation = models.BooleanField(default=False)
    override_translated_fields = models.BooleanField(default=False)

    class Meta(Model.Meta):
        abstract = True


class BasePageModel(Model, PageMixin):
    title = models.CharField(max_length=256, editable=False)
    slug = models.SlugField(max_length=128, unique=True, editable=False, db_index=True)
    folder_name = models.CharField(max_length=128, editable=False)
    subfolder_name = models.CharField(max_length=256, editable=False)
    body = models.TextField(editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta(Model.Meta):
        unique_together = ["folder_name", "subfolder_name"]
        ordering = ["folder_name", "-created_on"]
        abstract = True

    def __str__(self):
        return f"{self.folder_name}: {self.title}"
