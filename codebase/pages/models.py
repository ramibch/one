from auto_prefetch import ForeignKey
from django.db import models
from django.urls import reverse_lazy

from codebase.base.utils.abstracts import BasePageModel, BaseSubmodule


class PagesSubmodule(BaseSubmodule, submodule_name="pages"):
    """Pages submodule"""

    pass


class Page(BasePageModel, submodule_model=PagesSubmodule):
    """Page model"""

    submodule = ForeignKey(PagesSubmodule, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse_lazy("page-detail", kwargs={"slug": self.slug})
