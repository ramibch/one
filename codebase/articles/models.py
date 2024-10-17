from auto_prefetch import ForeignKey, Model
from base.abstracts import AbstractPage
from django.db import models
from markdownx.models import MarkdownxField


def upload_article_file(obj, filename):
    return f"articles/{obj.article.id}/{filename}"


class Article(AbstractPage):
    """Article page"""

    topic = models.CharField(max_length=128)
    folder = models.CharField(max_length=256)
    body = MarkdownxField()

    class Meta(AbstractPage.Meta):
        unique_together = ["topic", "folder"]


class ArticleFile(Model):
    article = ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to=upload_article_file)
    st_ctime = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
