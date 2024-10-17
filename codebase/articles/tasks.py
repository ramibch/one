from pathlib import Path

from django.conf import settings
from huey import crontab
from huey.contrib import djhuey as huey

from ..base.telegram import Bot


@huey.db_periodic_task(crontab(hour="0", minute="1"))
def sync_articles_dairly():
    """
    Read the contents of the 'articles' submodule and save them in the database.
    To know which contents to sync, check out the setting SYNC_ARTICLE_TOPICS.
    """

    # definitions and checks
    to_admin = "Syncing articles\n\n"

    topics = getattr(settings, ".SYNC_ARTICLE_TOPICS", ())

    if len(topics) == 0:
        Bot.to_admin(to_admin + "No topics found while syncing articles. Check SYNC_ARTICLE_TOPICS")
        return

    try:
        iter(topics)
    except TypeError:
        Bot.to_admin(to_admin + "The variable for topics is not iterable. Check SYNC_ARTICLE_TOPICS")
        return

    articles_path = getattr(settings, ".ARTICLES_MARKDOWN_PATH", None)

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
            to_admin += f"{topic} is not listed\n"
            continue

        for article_folder_path in topic_path.iterdir():
            if not article_folder_path.is_dir():
                continue

            for article_file_path in article_folder_path.iterdir():
                pass

                # article_file_path = topic_path / "how-to-example" / "en_.md"
                # article_file_path.stat().st_ctime <- compare -> article_obj.st_ctime

    Bot.to_admin(to_admin)
