from huey.contrib import djhuey as huey

from .models import Client


@huey.db_task()
def update_client_task(client: Client):
    """
    Update values of the client which were not proccessed in the `OneMiddleware`
    """
    client.update_values()
