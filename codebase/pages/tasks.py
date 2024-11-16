from huey import crontab
from huey.contrib import djhuey as huey

from ..utils.db_sync import sync_page_objects
from .models import Page


@huey.db_periodic_task(crontab(hour="2", minute="10"))
def sync_pages_daily():
    """Sync of pages in the db."""
    sync_page_objects(PageModel=Page)
