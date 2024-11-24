from auto_prefetch import Model
from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from .exceptions import SubmoduleException
from .mixins import PageMixin


def get_page_file_path(obj, filename: str):
    PageModel = obj.parent_page._meta.model
    submodule_name = PageModel.submodule_folder_model.submodule_name
    folder = obj.parent_page.folder
    subfolder = obj.parent_page.subfolder
    return f"{submodule_name}/{folder}/{subfolder}/{filename}"


class SubmodulesFolder(Model):
    submodule_name: str  # Override in the subclass.
    name = models.CharField(max_length=64, unique=True)

    class Meta(Model.Meta):
        abstract = True

    def __str__(self):
        return self.name

    @classmethod
    def sync_all_folders(cls):
        if cls == SubmodulesFolder:
            for SubmoduleFolderModel in cls.__subclasses__():
                SubmoduleFolderModel.sync_folders()
        else:
            print(f"⚠️  Just syncing for '{cls.submodule_name}'.")
            cls.sync_folders()

    @classmethod
    def sync_folders(cls):
        if cls == SubmodulesFolder:
            cls.sync_all_folders()
            return

        submodule_name = getattr(cls, "submodule_name", None)

        if submodule_name is None:
            raise SubmoduleException(f"Folder for {cls._meta.model} not found.")

        submodule_path = settings.SUBMODULES_PATH / submodule_name

        if not submodule_path.is_dir():
            raise SubmoduleException(f"Submodule {submodule_path} is not a directory")

        objs = []
        for folder_name in [f.name for f in submodule_path.iterdir() if f.is_dir()]:
            objs.append(cls._meta.model(name=folder_name))

        cls.objects.bulk_create(
            objs, update_fields=["name"], unique_fields=["name"], update_conflicts=True
        )


class PageModel(Model, PageMixin):
    submodule_folder_model: type[Model]  # Override in the subclass.
    submodule_folder: str  # Override in the subclass.

    title = models.CharField(max_length=256, editable=False)
    slug = models.SlugField(max_length=128, unique=True, editable=False, db_index=True)
    folder = models.CharField(max_length=128, editable=False)
    subfolder = models.CharField(max_length=256, editable=False)
    body = models.TextField(editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta(Model.Meta):
        unique_together = ["folder", "subfolder"]
        ordering = ["-created_on"]
        abstract = True


class PageFileModel(Model):
    parent_page = None  # Override in the subclass.
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to=get_page_file_path)

    class Meta(Model.Meta):
        abstract = True


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
    allow_translation = models.BooleanField(default=False)
    override_translated_fields = models.BooleanField(default=False)

    class Meta(Model.Meta):
        abstract = True

    @cached_property
    def extendedsite(self):
        from codebase.base.models import ExtendedSite

        if isinstance(self, ExtendedSite):
            return self

        if hasattr(self, "sites"):
            site = self.sites.first()
        elif hasattr(self, "site"):
            site = self.site
        return site.extendedsite

    @cached_property
    def default_language(self):
        return self.extendedsite.default_language

    @cached_property
    def rest_languages(self):
        return self.extendedsite.rest_languages

    @cached_property
    def languages(self):
        return self.extendedsite.languages

    @cached_property
    def languages_count(self):
        return self.extendedsite.languages_count
