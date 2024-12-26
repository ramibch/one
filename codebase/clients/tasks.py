from django.conf import settings
from huey import crontab
from huey.contrib import djhuey as huey

from .models import AutoBlockPath, Client


@huey.db_task()
def update_client_task(client: Client):
    """
    Update values of the client which were not proccessed in the `OneMiddleware`
    """
    client.update_values()


@huey.db_periodic_task(crontab(minute="47"))
def auto_block_clients_task_hourly():
    """
    Filter the clients which send requests to undesired paths and block them.
    """
    clients = Client.objects.filter(
        request__path__in=AutoBlockPath.objects.all(),
        ip_address__isnull=False,
    ).exclude(ip_address=Client.DUMMY_IP_ADDRESS)

    block_clients_task(clients)


@huey.db_task()
def block_clients_task(clients=None):
    """
    Block the selected clients
    """
    new_ipaddrs = list(clients.values_list("ip_address", flat=True).distinct())
    path = settings.BASE_DIR / "nginx/conf.d/blockips.conf"
    actual_ipaddrs = [
        line.replace("deny ", "").replace(";", "")
        for line in path.read_text().split("\n")
        if len(line) > 6
    ]
    ips = set(new_ipaddrs) | set(actual_ipaddrs)
    output_text = "".join({f"deny {ip};\n" for ip in ips})
    path.write_text(output_text)
    clients.update(is_blocked=True)
