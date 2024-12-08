from auto_prefetch import ForeignKey, Model
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from codebase.base.utils.abstracts import (
    BasePageModel,
    BaseSubmodule,
    PageFileModel,
)

User = get_user_model()


class ArticlesSubmodule(BaseSubmodule, submodule_name="articles"):
    """Submodule"""

    pass


class Article(BasePageModel, submodule_model=ArticlesSubmodule):
    """Article model"""

    submodule = ForeignKey(ArticlesSubmodule, on_delete=models.CASCADE)
    allow_comments = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    can_be_shown_in_home = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse_lazy("article-detail", kwargs={"slug": self.slug})


class ArticleFile(PageFileModel):
    """Article file model"""

    parent_page = ForeignKey(Article, on_delete=models.CASCADE)


class Comment(Model):
    article = ForeignKey(Article, on_delete=models.CASCADE)
    author = ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(_("Comment"), max_length=512)

    def __str__(self):
        return f"{self.content[:20]}... by {str(self.author)}"
