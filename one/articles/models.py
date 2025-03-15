from auto_prefetch import ForeignKey, Model
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from one.base import Languages
from one.base.utils.abstracts import BaseSubmoduleFolder, TranslatableModel
from one.base.utils.db import ChoiceArrayField

User = get_user_model()


class ArticleParentFolder(BaseSubmoduleFolder, submodule="articles"):
    """Parent folder of articles"""

    pass


class Article(TranslatableModel):
    """Article model"""

    language = models.CharField(
        max_length=4,
        choices=Languages,
        default=Languages.EN,
    )
    languages = ChoiceArrayField(
        models.CharField(max_length=8, choices=Languages),
        default=list,
        blank=True,
    )
    parent_folder = ForeignKey(ArticleParentFolder, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, editable=False)
    slug = models.SlugField(max_length=128, editable=False, db_index=True)
    folder_name = models.CharField(max_length=128, editable=False)
    subfolder_name = models.CharField(max_length=256, editable=False)
    body = models.TextField(editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    allow_comments = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse_lazy("article-detail", kwargs={"slug": self.slug})

    @cached_property
    def url(self):
        return self.get_absolute_url()

    def __str__(self):
        return f"{self.folder_name}/{self.subfolder_name}"

    @cached_property
    def has_equations(self):
        return "$$" in self.body


def get_article_file_path(obj, filename: str):
    folder = obj.article.folder_name
    subfolder = obj.article.subfolder_name
    return f"articles/{folder}/{subfolder}/{filename}"


class ArticleFile(Model):
    """Article file model"""

    article = ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to=get_article_file_path)

    def __str__(self):
        return self.name


class Comment(Model):
    article = ForeignKey(Article, on_delete=models.CASCADE)
    author = ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(_("Comment"), max_length=512)

    def __str__(self):
        return f"{self.content[:20]}... by {str(self.author)}"
