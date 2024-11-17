from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates initial menus"

    def add_arguments(self, parser):
        parser.add_argument("environments", nargs="+", type=str)

    def handle(self, *args, **options):
        sites = Site.objects.all()

        self.stdout.write(self.style.SUCCESS("Menus successfully created"))
