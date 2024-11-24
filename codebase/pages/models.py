from auto_prefetch import ForeignKey
from django.db import models
from django.urls import reverse_lazy

from codebase.base.utils.abstracts import PageModel, SubmodulesFolder, TranslatableModel


class PagesFolder(SubmodulesFolder):
    submodule_name = "pages"


class Page(PageModel, TranslatableModel):
    """File-based page model"""

    submodule_folder_model = PagesFolder
    submodule_folder = ForeignKey("pages.PagesFolder", on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse_lazy("page-detail", kwargs={"slug": self.slug})
