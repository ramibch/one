"""
Creates the default Site objects.
"""

from django.apps import apps as global_apps
from django.conf import settings
from django.db import DEFAULT_DB_ALIAS, router

HOSTS: list[str] = settings.ALLOWED_HOSTS


def create_default_sites(
    app_config,
    using=DEFAULT_DB_ALIAS,
    apps=global_apps,
    **kwargs,
):
    try:
        Site = apps.get_model("sites", "Site")
        Domain = apps.get_model("sites", "Domain")
    except LookupError:
        return

    if not router.allow_migrate_model(using, Site):
        return

    if Site.objects.using(using).exists():
        print("Site objects exist already")
        return

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
        site = Site(name=site_name)
        site.save(using=using)
        domain = Domain(site=site, name=domain_name)
        domain.save(using=using)

        if f"www.{domain_name}" in HOSTS:
            wwwdomain = Domain(site=site, name=f"www.{domain_name}")
            wwwdomain.save(using=using)
