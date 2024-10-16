from auto_prefetch import ForeignKey, Model
from django.db import models
from markdownx.models import MarkdownxField

from base.abstracts import AbstractPage


def upload_article_file(obj, filename):
    return f"articles/{obj.article.id}/{filename}"


class Article(AbstractPage):
    """Article page"""

    body = MarkdownxField(null=True)


class ArticleFile(Model):
    article = ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, null=True)

    file = models.FileField(upload_to=upload_article_file)

    def __str__(self):
        return self.name
