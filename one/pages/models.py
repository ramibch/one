from auto_prefetch import ForeignKey, Model
from django.db import models
from django.urls import reverse_lazy

from one.base.utils.abstracts import BaseSubmoduleFolder
from one.base.utils.mixins import PageMixin


class PageParentFolder(BaseSubmoduleFolder, submodule="pages"):
    """Pages submodule"""

    pass


class Page(Model, PageMixin):
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
