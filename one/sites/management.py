"""
Creates the default Site objects.
"""

from django.apps import apps as global_apps
from django.conf import settings
from django.db.utils import IntegrityError


def create_sites_and_necessary_objects(app_config, apps=global_apps, **kwargs):
    from ..home.models import Home
    from .models import Site

    for host in settings.ALLOWED_HOSTS:
        try:
            site = Site.objects.get(domain=host)
        except (IntegrityError, Site.DoesNotExist):
            site = Site.objects.create(domain=host)

        Home.objects.get_or_create(site=site)
