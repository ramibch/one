"""
Creates the default Site objects.
"""

from django.apps import apps as global_apps
from django.conf import settings
from django.db.utils import IntegrityError

HOSTS: list[str] = settings.ALLOWED_HOSTS


def create_sites_and_necessary_objects(app_config, apps=global_apps, **kwargs):
    from ..home.models import Home
    from .models import Site

    # Hosts with "www." are processed in an other way (check below).
    host_names = []
    for host in HOSTS:
        if host in ["localhost", "127.0.0.1"] and settings.ENV == "dev":
            for port in (8000, 8001, 8002):
                host_names.append(f"{host}:{port}")
        host_names.append(host)

    # There may be a better way to do this, but for few objects is fine.
    for host_name in host_names:
        try:
            site = Site.objects.get(domain=host_name)
        except (IntegrityError, Site.DoesNotExist):
            site = Site.objects.create(domain=host_name)

        Home.objects.get_or_create(site=site)
