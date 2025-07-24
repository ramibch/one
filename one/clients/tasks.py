from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Count, Max, Q
from django.utils import timezone
from huey import crontab
from huey.contrib import djhuey as huey

from ..bot import Bot
from ..sites.models import Site
from .models import Client, Path, Request

User = get_user_model()


@huey.db_task()
def save_request_task(params):
    try:
        req = Request()
        pn = params.get("path_name")
        req.path = Path.objects.get_or_create(name=pn)[0]
        params.pop("path_name")

        for k, v in params.items():
            setattr(req, k, v)
        req.save()
    except Exception as e:  # pragma: no cover
        Bot.to_admin(f"Error by saving request obj: {e}")


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
            site=site,
            path__is_spam=True,
            time__lt=now - site.spam_requests_duration,
        )

        qs = qs | Request.objects.filter(
            site=site,
            time__lt=now - site.requests_duration,
        )

    out = qs.distinct().delete()
    if out[0] > 0:
        Bot.to_admin(f"{out[0]} Requests purged")


@huey.db_periodic_task(crontab(day="15", hour="15", minute="15"))
def inform_admin_about_404_issues():
    dt_diff = Site.objects.aggregate(Max("requests_duration")).get(
        "requests_duration__max"
    )

    some_time_ago = timezone.now() - dt_diff  # type: ignore

    qs = (
        Path.objects.annotate(
            num=Count(
                "request",
                filter=Q(
                    request__status_code=404,
                    request__time__gt=some_time_ago,
                ),
            )
        )
        .filter(is_spam=False)
        .order_by("-num")[0:100]
    )
    text = "Most not-found (404) paths\n\n"
    text += "\n".join(f"{p.num} {p.name}" for p in qs)  # type: ignore
    Bot.to_admin(text)
