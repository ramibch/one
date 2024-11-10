from auto_prefetch import ForeignKey, Model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from markdownx.models import MarkdownxField

from .constants import DJANGO_URL_PATHS


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


class AbstractLinkModel(Model):
    custom_title = models.CharField(max_length=128, null=True, blank=True)
    external_url = models.URLField(max_length=256, null=True, blank=True)
    django_url_path = models.CharField(blank=True, null=True, max_length=32, choices=DJANGO_URL_PATHS)
    page = ForeignKey("pages.Page", on_delete=models.CASCADE, null=True, blank=True)
    plan = ForeignKey("plans.Plan", on_delete=models.CASCADE, null=True, blank=True)
    article = ForeignKey("articles.Article", on_delete=models.CASCADE, null=True, blank=True)
    new_tab = models.BooleanField(default=False)
    allow_field_translation = models.BooleanField(default=False)

    class Meta(Model.Meta):
        abstract = True

    def __str__(self):
        return f"<Link to {self.title}>"

    def clean_custom_title(self):
        if self.external_url and self.custom_title is None:
            raise ValidationError(_("Enter a custom title if an external url is entered."), code="invalid")

    def clean(self):
        if self.link_fields.count(None) != self.count_link_fields - 1:
            raise ValidationError(_("One link must be entered."), code="invalid")
        super().clean()

    @cached_property
    def model_object_fields(self):
        return [self.page, self.plan, self.article]

    @cached_property
    def other_link_fields(self):
        return [self.django_url_path, self.external_url]

    @cached_property
    def link_fields(self):
        return self.model_object_fields + self.other_link_fields

    @cached_property
    def count_link_fields(self):
        return len(self.link_fields)

    @cached_property
    def model_obj(self):
        return next((obj for obj in self.model_object_fields if obj is not None), None)

    @cached_property
    def url(self):
        if self.django_url_path:
            return reverse_lazy(self.django_url_path)

        if self.external_url:
            return self.external_url

        if self.model_obj:
            return self.model_obj.url

    @cached_property
    def title(self):
        if self.django_url_path:
            return self.get_django_url_path_display()

        if self.custom_title:
            return self.custom_title

        if self.model_obj:
            return self.model_obj.title


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
