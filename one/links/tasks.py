from huey import crontab
from huey.contrib import djhuey as huey

from one.base.utils.telegram import Bot

from .models import Link


@huey.db_periodic_task(crontab(hour="3", minute="1"))
def sync_django_links():
    Link.objects.sync_django_paths()


@huey.db_periodic_task(crontab(hour="8", minute="3"))
def check_empty_links():
    qs = Link.objects.filter(
        url_path__isnull=True,
        external_url__isnull=True,
        topic__isnull=True,
        landing__isnull=True,
        product__isnull=True,
    )

    if qs.count() > 0:
        Bot.to_admin("⚠️ There are empty links in the application!")
