from huey import crontab
from huey.contrib import djhuey as huey

from .models import Link


@huey.db_periodic_task(crontab(hour="3", minute="1"))
def sync_django_links():
    Link.objects.sync_django_paths()
