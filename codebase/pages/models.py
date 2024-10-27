from django.urls import reverse_lazy

from ..utils.abstracts import AbstractPage


class Page(AbstractPage):
    """File-based page model"""

    def get_absolute_url(self):
        return reverse_lazy("page-detail", kwargs={"slug": self.slug})
