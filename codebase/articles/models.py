from auto_prefetch import ForeignKey, Model
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from codebase.base.utils.abstracts import (
    BasePageModel,
    BaseSubmoduleFolder,
)

User = get_user_model()


class ArticleParentFolder(BaseSubmoduleFolder, submodule="articles"):
    """Parent folder of articles"""

    pass


class Article(BasePageModel):
    """Article model"""

    parent_folder = ForeignKey("articles.ArticleParentFolder", on_delete=models.CASCADE)
    allow_comments = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    can_be_shown_in_home = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse_lazy("article-detail", kwargs={"slug": self.slug})


def get_article_file_path(obj, filename: str):
    folder = obj.article.folder_name
    subfolder = obj.article.subfolder_name
    return f"articles/{folder}/{subfolder}/{filename}"


class ArticleFile(Model):
    """Article file model"""

    article = ForeignKey("articles.Article", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to=get_article_file_path)

    def __str__(self):
        return self.name


class Comment(Model):
    article = ForeignKey("articles.Article", on_delete=models.CASCADE)
    author = ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(_("Comment"), max_length=512)

    def __str__(self):
        return f"{self.content[:20]}... by {str(self.author)}"
