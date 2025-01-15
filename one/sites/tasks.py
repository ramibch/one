from huey import crontab
from huey.contrib import djhuey as huey

from one.sites.models import Site

from ..base.utils.telegram import Bot


@huey.db_periodic_task(crontab(hour="0", minute="15"))
def check_sites_without_homes_daily():
    sites = Site.objects.filter(home__isnull=True)
    if sites.count() > 0:
        sites_str = "\n".join(site.name for site in sites)
        msg = f"⚠️ These sites have no Home associated:\n\n{sites_str}"
        Bot.to_admin(msg)
