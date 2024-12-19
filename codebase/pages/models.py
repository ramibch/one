from auto_prefetch import ForeignKey
from django.db import models
from django.urls import reverse_lazy

from codebase.base.utils.abstracts import BasePageModel, BaseSubmoduleFolder


class PageParentFolder(BaseSubmoduleFolder, submodule="pages"):
    """Pages submodule"""

    pass


class Page(BasePageModel):
    """Page model"""

    parent_folder = ForeignKey("pages.PageParentFolder", on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse_lazy("page-detail", kwargs={"slug": self.slug})
