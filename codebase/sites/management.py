"""
Creates the default Site objects.
"""

from django.apps import apps as global_apps
from django.conf import settings
from django.db.utils import IntegrityError

HOSTS: list[str] = settings.ALLOWED_HOSTS


def create_sites_and_necessary_objects(app_config, apps=global_apps, **kwargs):
    from ..home.models import Home, UserHome
    from .models import Domain, Site

    domain_names_without_wwws = []
    for host in HOSTS:
        if host in ["localhost", "127.0.0.1"] and settings.ENV == "dev":
            for port in (8000, 8001, 8002):
                domain_names_without_wwws.append(f"{host}:{port}")
        elif not host.startswith("www."):
            # Hosts with "www." are processed in an other way (check below).
            domain_names_without_wwws.append(host)

    # There may be a better way to do this, but for few objects is fine.
    for domain_name in domain_names_without_wwws:
        try:
            domain = Domain.objects.get_or_create(name=domain_name)[0]
            site = domain.site
        except IntegrityError:
            site = Site.objects.get_or_create(name=domain_name)[0]
            domain = Domain.objects.get_or_create(name=domain_name, site=site)[0]

        www_domain_name = f"www.{domain_name}"
        if www_domain_name in HOSTS:
            Domain.objects.get_or_create(site=site, name=www_domain_name, is_main=False)

        Home.objects.get_or_create(site=site)
        UserHome.objects.get_or_create(site=site)
