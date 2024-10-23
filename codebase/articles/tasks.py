from huey import crontab
from huey.contrib import djhuey as huey

from .models import sync_articles


@huey.db_periodic_task(crontab(hour="1", minute="10"))
def sync_articles_dairly():
    sync_articles()
