"""
Creates the default Site objects.
"""

from django.apps import apps as global_apps
from django.conf import settings
from django.db.utils import IntegrityError

HOSTS: list[str] = settings.ALLOWED_HOSTS


def create_sites_and_necessary_objects(app_config, apps=global_apps, **kwargs):
    from ..home.models import Home
    from .models import Host, Site

    # Hosts with "www." are processed in an other way (check below).
    host_names_without_wwws = []
    for host in HOSTS:
        if host in ["localhost", "127.0.0.1"] and settings.ENV == "dev":
            for port in (8000, 8001, 8002):
                host_names_without_wwws.append(f"{host}:{port}")
        elif not host.startswith("www."):
            host_names_without_wwws.append(host)

    # There may be a better way to do this, but for few objects is fine.
    for host_name in host_names_without_wwws:
        try:
            host = Host.objects.get_or_create(name=host_name)[0]
            site = host.site
        except IntegrityError:
            site = Site.objects.get_or_create(name=host_name)[0]
            host = Host.objects.get_or_create(name=host_name, site=site)[0]

        www_host_name = f"www.{host_name}"
        if www_host_name in HOSTS:
            Host.objects.get_or_create(site=site, name=www_host_name, is_main=False)

        Home.objects.get_or_create(site=site)
