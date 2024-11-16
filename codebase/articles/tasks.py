from huey import crontab
from huey.contrib import djhuey as huey

from ..utils.db_sync import sync_page_objects
from .models import Article, ArticleFile


@huey.db_periodic_task(crontab(hour="1", minute="10"))
def sync_articles_daily():
    """Sync of articles in the db."""
    sync_page_objects(PageModel=Article, PageModelFile=ArticleFile)
