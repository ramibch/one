from auto_prefetch import Model
from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from django.utils.html import format_html
from markdownx.models import MarkdownxField


class AbstractPage(Model):
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

    def get_absolute_url(self):
        raise NotImplementedError("This method is not implemented in the AbstractPage model.")

    @cached_property
    def url(self):
        return self.get_absolute_url()

    @cached_property
    def anchor_tag(self):
        return format_html(f"<a target='_blank' href='{self.url}'>{self.title}</a>")

    @cached_property
    def full_page_url(self):
        return settings.WEBSITE_URL + self.url

    def __str__(self):
        return self.title


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
