from auto_prefetch import ForeignKey, Model
from django.conf import settings
from django.db import models
from django.urls import reverse_lazy
from django.utils.functional import cached_property

from one.base.utils.abstracts import BaseSubmoduleFolder

SUBMODULE_NAME = "pages" if settings.ENV == "prod" else "test-pages"


class PageParentFolder(BaseSubmoduleFolder, submodule=SUBMODULE_NAME):
    """Pages submodule"""

    pass


class Page(Model):
    """Page model"""

    parent_folder = ForeignKey("pages.PageParentFolder", on_delete=models.CASCADE)

    title = models.CharField(max_length=256, editable=False)
    slug = models.SlugField(
        max_length=128,
        editable=False,
        db_index=True,
        null=True,
        blank=True,
    )
    folder_name = models.CharField(max_length=128, editable=False)
    subfolder_name = models.CharField(max_length=256, editable=False)
    body = models.TextField(editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse_lazy("page-detail", kwargs={"slug": self.slug})

    @cached_property
    def url(self):
        return self.get_absolute_url()
