from huey import crontab
from huey.contrib import djhuey as huey

from .models import Client


@huey.db_periodic_task(crontab(hour="45"))
def assign_countries_to_clients(clients=None):
    if clients is None:
        clients = Client.objects.filter(country__isnull=True)

    for client in clients:
        client = client.update_country()
