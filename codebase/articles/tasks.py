from huey import crontab
from huey.contrib import djhuey as huey

from codebase.base.utils.db_sync import sync_page_objects

from .models import Article, ArticleFile


@huey.db_periodic_task(crontab(hour="1", minute="10"))
def sync_articles_daily():
    """Daily task to sync articles from the submodule for articles to the db."""
    sync_page_objects(PageModel=Article, PageModelFile=ArticleFile)


@huey.task()
def trigger_sync_articles(extsites):
    sync_page_objects(
        PageModel=Article, PageModelFile=ArticleFile, extended_sites=extsites
    )
