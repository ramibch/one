from auto_prefetch import ForeignKey, Model
from django.db import models

from ..base.abstracts import AbstractPage

def upload_article_file(obj, filename:str):
    return f"articles/{obj.article.folder}/{obj.article.subfolder}/{filename}"


class Article(AbstractPage):
    """File-based article model"""
    pass


class ArticleFile(Model):
    article = ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to=upload_article_file)

    def __str__(self):
        return self.name



