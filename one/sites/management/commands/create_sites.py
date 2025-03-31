from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from one.sites.models import Site


class Command(BaseCommand):
    help = "Creates the default Site objects."

    def handle(self, *args, **options):
        for host in settings.ALLOWED_HOSTS:
            try:
                Site.objects.get(domain=host)
            except (IntegrityError, Site.DoesNotExist):
                Site.objects.create(domain=host)
