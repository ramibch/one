from auto_prefetch import ForeignKey
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from one.db import BaseSubmoduleFolder, ChoiceArrayField, OneModel, TranslatableModel

User = get_user_model()


class MainTopic(BaseSubmoduleFolder, submodule="articles"):
    """
    Parent folder of articles

    The name attr is the topic
    """

    pass


class Article(TranslatableModel):
    """Article model"""

    LANGS_ATTR = "languages"
    # LANG_ATTR = "language"

    languages = ChoiceArrayField(
        models.CharField(max_length=8, choices=settings.LANGUAGES),
        default=list,
        blank=True,
    )
    main_topic = ForeignKey(MainTopic, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, editable=False)
    slug = models.SlugField(max_length=128, editable=False, db_index=True)
    folder_name = models.CharField(max_length=128, editable=False)
    subfolder_name = models.CharField(max_length=256, editable=False)
    body = models.TextField(editable=False)
    allow_comments = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.folder_name}/{self.subfolder_name}"

    def get_absolute_url(self):
        slug = self.slug or self.get_fallback_value("slug")
        return reverse_lazy("slug_page", kwargs={"slug": slug})

    @property
    def fallback_body(self):
        return self.get_fallback_value("body")

    @property
    def fallback_title(self):
        return self.get_fallback_value("title")

    @property
    def display_title(self):
        return self.title or self.fallback_title

    @property
    def display_body(self):
        return self.body or self.fallback_body

    @property
    def url(self):
        return self.get_absolute_url()

    @property
    def has_equations(self):
        return "$$" in self.display_body


def get_article_file_path(obj, filename: str):
    folder = obj.article.folder_name
    subfolder = obj.article.subfolder_name
    return f"articles/{folder}/{subfolder}/{filename}"


class ArticleFile(OneModel):
    """Article file model"""

    article = ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to=get_article_file_path)

    def __str__(self):
        return self.name


class Comment(OneModel):
    article = ForeignKey(Article, on_delete=models.CASCADE)
    author = ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(_("Comment"), max_length=512)

    def __str__(self):
        return f"{self.content[:20]}... by {str(self.author)}"
