"""
Creates the default Site objects.
"""

from django.apps import apps as global_apps
from django.conf import settings

HOSTS: list[str] = settings.ALLOWED_HOSTS


def create_default_sites(app_config, apps=global_apps, **kwargs):
    from .models import Domain, Site

    sites_and_domains = []
    for host in HOSTS:
        if host in ["localhost", "127.0.0.1"] and settings.ENV == "dev":
            for port in (8000, 8001, 8002):
                sites_and_domains.append((f"Site {host}:{port}", f"{host}:{port}"))
        elif not host.startswith("www."):
            # Hosts with "www." are processed in an other way (check below).
            sites_and_domains.append((f"Site {host}", host))

    # There may be a better way to do this, but for few objects is fine.
    for site_name, domain_name in sites_and_domains:
        wwwhost = f"www.{domain_name}"
        site = Site.objects.get_or_create(name=site_name)[0]
        Domain.objects.get_or_create(site=site, name=domain_name)
        if wwwhost in HOSTS:
            Domain.objects.get_or_create(site=site, name=wwwhost, is_main=False)
