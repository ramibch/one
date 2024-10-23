from pathlib import Path

from auto_prefetch import ForeignKey, Model
from django.conf import settings
from django.core.files import File
from django.db import models
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from ..base.abstracts import AbstractPage
from ..base.telegram import Bot


def upload_article_file(obj, filename: str):
    return f"articles/{obj.article.folder}/{obj.article.subfolder}/{filename}"


class Article(AbstractPage):
    """File-based article model"""

    featured = models.BooleanField(_("Featured article"), help_text=_("If featured it will be showed in home "), default=False)

    def get_absolute_url(self):
        return reverse_lazy("article-detail", kwargs={"slug": self.slug})


class ArticleFile(Model):
    article = ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to=upload_article_file)

    def __str__(self):
        return self.name


def sync_articles():
    """
    Read the contents of the 'articles' submodule and save them in the database.
    To know which contents to sync, check out the setting SYNC_ARTICLE_FOLDERS.
    """

    # definitions and checks
    to_admin = "🔄 Syncing articles\n\n"

    folders = getattr(settings, "SYNC_ARTICLE_FOLDERS", ())

    if len(folders) == 0:
        Bot.to_admin(to_admin + "No folders found while syncing articles. Check SYNC_ARTICLE_FOLDERS")
        return

    try:
        iter(folders)
    except TypeError:
        Bot.to_admin(to_admin + "The variable for folders is not iterable. Check SYNC_ARTICLE_FOLDERS")
        return

    articles_path = getattr(settings, "ARTICLES_MARKDOWN_PATH", None)

    if not isinstance(articles_path, Path):
        Bot.to_admin(to_admin + "No path for articles found. Check ARTICLES_MARKDOWN_PATH")
        return

    if not articles_path.is_dir():
        Bot.to_admin(to_admin + "The 'articles' path is not a directory. Check ARTICLES_MARKDOWN_PATH")
        return

    # Scanning
    for folder in folders:
        folder_path = articles_path / folder

        if not folder_path.is_dir():
            to_admin += f"🔴 {folder} is not listed\n\n"
            continue

        for subfolder_path in folder_path.iterdir():
            if not subfolder_path.is_dir():
                continue

            body_replacements = {}
            to_admin += f"✍ {folder}/{subfolder_path.name}\n"
            db_article = Article.objects.get_or_create(folder=folder, subfolder=subfolder_path.name)[0]

            # Markdown files (.md) need to be proccessed first
            for md_file_path in (p for p in subfolder_path.iterdir() if p.name.endswith(".md")):
                md_file_conventions_ok = all(
                    (
                        md_file_path.name[:2] in settings.LANGUAGE_CODES,
                        len(md_file_path.read_text().split("\n")) > 2,
                        md_file_path.read_text().strip().startswith("#"),
                    )
                )
                if not md_file_conventions_ok:
                    to_admin += f"⚠️ File '{md_file_path.name}' does not meet conventions"
                    continue

                lang_code = md_file_path.name[:2]
                title = md_file_path.read_text().split("\n")[0].replace("#", "").strip()
                body_text = "\n".join(md_file_path.read_text().split("\n")[1:]).strip()
                setattr(db_article, f"title_{lang_code}", title)
                setattr(db_article, f"slug_{lang_code}", slugify(title))
                setattr(db_article, f"body_{lang_code}", body_text)

            # The other files are proccessed afterwards
            for other_file_path in (p for p in subfolder_path.iterdir() if not p.name.endswith(".md")):
                db_articlefile = ArticleFile.objects.get_or_create(article=db_article, name=other_file_path.name)[0]
                db_articlefile.file = File(other_file_path.open(mode="rb"), name=other_file_path.name)
                db_articlefile.save()
                body_replacements[f"]({db_articlefile.name})"] = f"]({db_articlefile.file.url})"

            # Adjust article body field if the markdown file includes files.
            for local, remote in body_replacements.items():
                for lang_code in settings.LANGUAGE_CODES:
                    new_value = getattr(db_article, f"body_{lang_code}").replace(local, remote)
                    setattr(db_article, f"body_{lang_code}", new_value)

            # Save all object attributes in the database
            db_article.save()

    # Delete articles that could not be processed
    qs = Article.objects.filter(Q(title__in=[None, ""]) | Q(body__in=[None, ""]))
    if qs.count() > 0:
        to_admin += "\n😔Articles not possible to create:\n"
    for obj in qs:
        to_admin += f"{obj.folder}/{obj.subfolder}\n"
    qs.delete()

    Bot.to_admin(to_admin)
