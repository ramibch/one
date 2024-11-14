from auto_prefetch import Manager, Model
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import cached_property
from django.utils.html import format_html
from markdownx.models import MarkdownxField

from ..utils.exceptions import SubmoduleException

User = get_user_model()


class SubmoduleFolderManager(Manager):
    def _get_submodule(self):
        from ..articles.models import ArticleFolder
        from ..pages.models import PageFolder

        SUBMODULES = {
            ArticleFolder: "articles",
            PageFolder: "pages",
        }
        try:
            return SUBMODULES[self.model]
        except KeyError as e:
            raise e

    def sync_folders(self):
        submodule = self._get_submodule()

        if submodule is None:
            raise SubmoduleException(f"Submodule for {self.model} not found")

        submodule_path = settings.SUBMODULES_PATH / submodule

        if not submodule_path.is_dir():
            raise SubmoduleException(f"Submodule {submodule_path} is not a directory")

        objs = []
        for folder_name in [f.name for f in submodule_path.iterdir() if f.is_dir()]:
            objs.append(self.model(name=folder_name))

        self.bulk_create(objs, update_fields=["name"], unique_fields=["name"], update_conflicts=True)


class AbstractFolder(Model):
    name = models.CharField(max_length=64, unique=True)
    objects = SubmoduleFolderManager()

    class Meta(Model.Meta):
        abstract = True

    def __str__(self):
        return self.name


class PageMixin:
    title = "Please override title field in the subclass."

    def get_absolute_url(self):
        raise NotImplementedError

    @cached_property
    def url(self):
        return self.get_absolute_url()

    @cached_property
    def anchor_tag(self):
        return format_html(f"<a target='_blank' href='{self.url}'>{self.title}</a>")

    def __str__(self):
        return self.title


class AbstractFlatPageModel(Model, PageMixin):
    title = models.CharField(max_length=256, editable=False)
    slug = models.SlugField(max_length=128, unique=True, editable=False)
    folder = models.CharField(max_length=128, editable=False)
    subfolder = models.CharField(max_length=256, editable=False)
    body = MarkdownxField(editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta(Model.Meta):
        unique_together = ["folder", "subfolder"]
        ordering = ["-created_on"]
        abstract = True


class AbstractSingletonModel(Model):
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
