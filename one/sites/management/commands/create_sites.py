from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from one.home.models import Home
from one.sites.models import Site


class Command(BaseCommand):
    help = "Creates the default Site objects."

    def handle(self, *args, **options):
        for host in settings.ALLOWED_HOSTS:
            try:
                site = Site.objects.get(domain=host)
            except (IntegrityError, Site.DoesNotExist):
                site = Site.objects.create(domain=host)

            Home.objects.get_or_create(site=site)
