from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from huey import crontab
from huey.contrib import djhuey as huey

from ..base.utils.telegram import Bot
from ..sites.models import Site
from .models import Client, Request


@huey.db_task()
def update_client_task(client: Client):
    """
    Update values of the client which were not proccessed in the `OneMiddleware`
    """
    client.update_values()


@huey.db_periodic_task(crontab(minute="47"))
def block_spammy_clients_hourly():
    """
    Filter the clients which send requests to undesired paths and block them.
    """
    clients = Client.objects.filter(request__path__is_spam=True).exclude(
        ip_address=Client.DUMMY_IP_ADDRESS
    )
    block_spammy_clients(clients)


@huey.db_task()
def block_spammy_clients(clients=None):
    """
    Block the selected clients
    """
    if clients is None:
        clients = Client.objects.filter(is_blocked=True)

    clients = clients.filter(ip_address__isnull=False)
    new_ipaddrs = list(clients.values_list("ip_address", flat=True).distinct())
    path = settings.BASE_DIR / "nginx/conf.d/blockips.conf"
    actual_ipaddrs = [
        line.replace("deny ", "").replace(";", "")
        for line in path.read_text().split("\n")
        if len(line) > 6
    ]
    ips = set(new_ipaddrs) | set(actual_ipaddrs)
    cache.set("blocked_ips", ips, 86400)
    output_text = "".join({f"deny {ip};\n" for ip in ips})
    path.write_text(output_text)
    clients.update(is_blocked=True)


@huey.db_periodic_task(crontab(hour="1", minute="15"))
def purge_requests_task():
    """Purge requests"""
    now = timezone.now()
    qs = Request.objects.none()

    for site in Site.objects.all():
        qs = qs | Request.objects.filter(
            client__site=site,
            path__is_spam=True,
            time__lt=now - site.spam_requests_duration,
        )

        qs = qs | Request.objects.filter(
            client__site=site,
            time__lt=now - site.requests_duration,
        )

    out = qs.distinct().delete()
    if out[0] > 0:
        Bot.to_admin(f"{out[0]} Requests purged")
