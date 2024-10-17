from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.db.models import Q
from huey import crontab
from huey.contrib import djhuey as huey

from ..base.telegram import Bot
from .models import Article, ArticleFile


def check_article_file_conventions(article_file_path: Path) -> bool:
    return all(
        (
            article_file_path.name[:2] in settings.LANGUAGE_CODES,
            len(article_file_path.read_text().split("\n")),
            article_file_path.read_text().strip().startswith("#"),
        )
    )


@huey.db_periodic_task(crontab(hour="0", minute="1"))
def sync_articles_dairly___():
    pass


def sync_articles_dairly():
    """
    Read the contents of the 'articles' submodule and save them in the database.
    To know which contents to sync, check out the setting SYNC_ARTICLE_TOPICS.
    """

    # definitions and checks
    to_admin = "🔄 Syncing articles\n\n"

    topics = getattr(settings, "SYNC_ARTICLE_TOPICS", ())

    if len(topics) == 0:
        Bot.to_admin(to_admin + "No topics found while syncing articles. Check SYNC_ARTICLE_TOPICS")
        return

    try:
        iter(topics)
    except TypeError:
        Bot.to_admin(to_admin + "The variable for topics is not iterable. Check SYNC_ARTICLE_TOPICS")
        return

    articles_path = getattr(settings, "ARTICLES_MARKDOWN_PATH", None)

    if not isinstance(articles_path, Path):
        Bot.to_admin(to_admin + "No path for articles found while syncing articles. Check ARTICLES_MARKDOWN_PATH")
        return

    if not articles_path.is_dir():
        Bot.to_admin(to_admin + "The 'articles' path is not a directory. Check ARTICLES_MARKDOWN_PATH")
        return

    # Scanning
    for topic in topics:
        topic_path = articles_path / topic

        if not topic_path.is_dir():
            to_admin += f"🔴 {topic} is not listed\n\n"
            continue

        for folder_path in topic_path.iterdir():
            if not folder_path.is_dir():
                continue

            to_admin += f"✍ {topic}/{folder_path.name}\n"
            body_replacements = {}

            # We make sure that we proccess the markdown files first!
            article_file_paths = [p for p in list(folder_path.iterdir()) if p.name.endswith(".md")] + [
                p for p in list(folder_path.iterdir()) if not p.name.endswith(".md")
            ]
            for file_path in article_file_paths:
                db_article = Article.objects.get_or_create(topic=topic, folder=folder_path.name)[0]

                if file_path.name.endswith(".md"):
                    if not check_article_file_conventions(file_path):
                        to_admin += f"⚠️ File '{file_path.name}' does not meet conventions"
                        continue

                    lang_code = file_path.name[:2]
                    title = file_path.read_text().split("\n")[0].replace("#", "").strip()
                    body_text = "\n".join(file_path.read_text().split("\n")[1:]).strip()
                    setattr(db_article, f"title_{lang_code}", title)
                    setattr(db_article, f"body_{lang_code}", body_text)
                    setattr(db_article, "folder", folder_path.name)
                    setattr(db_article, "topic", topic)
                else:
                    db_articlefile = ArticleFile.objects.get_or_create(article=db_article, name=file_path.name)[0]
                    db_articlefile.file = File(file_path.open(mode="rb"), name=file_path.name)
                    db_articlefile.save()
                    body_replacements[f"]({db_articlefile.name})"] = f"]({db_articlefile.file.url})"

                if body_replacements != {}:
                    for lang_code in settings.LANGUAGE_CODES:
                        for local, remote in body_replacements.items():
                            value = getattr(db_article, f"body_{lang_code}").replace(local, remote)
                            setattr(db_article, f"body_{lang_code}", value)

                db_article.save()

    # Delete articles that could not be processed
    qs = Article.objects.filter(Q(title__in=[None, ""]) | Q(body__in=[None, ""]))
    if qs.count() > 0:
        to_admin += "\n😔Articles not possible to create:\n"
    for obj in qs:
        to_admin += f"{obj.topic}/{obj.folder}"
    qs.delete()

    Bot.to_admin(to_admin)
