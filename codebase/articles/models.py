from auto_prefetch import ForeignKey, Model
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..base.abstracts import AbstractPage


def upload_article_file(obj, filename: str):
    return f"articles/{obj.article.folder}/{obj.article.subfolder}/{filename}"


class Article(AbstractPage):
    """File-based article model"""

    featured = models.BooleanField(_("Featured article"), help_text=_("If featured it will be showed in home "), default=False)


class ArticleFile(Model):
    article = ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to=upload_article_file)

    def __str__(self):
        return self.name
