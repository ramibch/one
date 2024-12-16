from django.db.models import Q
from huey import crontab
from huey.contrib import djhuey as huey

from codebase.sites.models import Site

from ..base.utils.telegram import Bot


@huey.db_periodic_task(crontab(hour="0", minute="15"))
def check_sites_without_homes_daily():
    sites = Site.objects.filter(Q(home__isnull=True) | Q(userhome__isnull=True))
    sites_str = "\n".join(site.name for site in sites)
    msg = f"⚠️ These sites have no Home and/or UserHome associated:\n\n{sites_str}"
    Bot.to_admin(msg)
