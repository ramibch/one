from auto_prefetch import ForeignKey, Model
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from ..utils.abstracts import (
    PageFileModel,
    PageModel,
    SubmodulesFolder,
)

User = get_user_model()


def upload_article_file(obj, filename: str):
    return f"articles/{obj.parent_page.folder}/{obj.parent_page.subfolder}/{filename}"


class ArticlesFolder(SubmodulesFolder):
    submodule_name = "articles"


class Article(PageModel):
    """
    File-based article model
    """

    submodule_folder_model = ArticlesFolder
    submodule_folder = ForeignKey(ArticlesFolder, on_delete=models.SET_NULL, null=True)

    sites = models.ManyToManyField(Site)
    featured = models.BooleanField(
        _("Featured article"),
        help_text=_("If featured it will be showed in home "),
        default=False,
    )
    allow_comments = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    can_be_shown_in_home = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse_lazy("article-detail", kwargs={"slug": self.slug})


class ArticleFile(PageFileModel):
    parent_page = ForeignKey(Article, on_delete=models.CASCADE)


class Comment(Model):
    article = ForeignKey(Article, on_delete=models.CASCADE)
    author = ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(_("Comment"), max_length=512)

    def __str__(self):
        return f"{self.content[:20]}... by {str(self.author)}"
