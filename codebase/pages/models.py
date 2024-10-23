from ..base.abstracts import AbstractPage

from django.urls import reverse_lazy

class Page(AbstractPage):
    """File-based page model"""

    def get_absolute_url(self):
        return reverse_lazy("page-detail", kwargs={"slug": self.slug})
