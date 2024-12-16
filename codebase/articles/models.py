from auto_prefetch import ForeignKey, Model
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from codebase.base.utils.abstracts import (
    BasePageFileModel,
    BasePageModel,
    BaseSubmodule,
)

User = get_user_model()


class ArticleParentFolder(BaseSubmodule, submodule_name="articles"):
    """Submodule"""

    pass


class Article(BasePageModel, parent_model=ArticleParentFolder):
    """Article model"""

    parent = ForeignKey("articles.ArticleParentFolder", on_delete=models.CASCADE)
    allow_comments = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    can_be_shown_in_home = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse_lazy("article-detail", kwargs={"slug": self.slug})


class ArticleFile(BasePageFileModel):
    """Article file model"""

    parent = ForeignKey("articles.Article", on_delete=models.CASCADE)


class Comment(Model):
    article = ForeignKey("articles.Article", on_delete=models.CASCADE)
    author = ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(_("Comment"), max_length=512)

    def __str__(self):
        return f"{self.content[:20]}... by {str(self.author)}"
