from django.utils.functional import cached_property
from django.utils.html import format_html


class PageMixin:
    title = None  # Override title field in the subclass

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
