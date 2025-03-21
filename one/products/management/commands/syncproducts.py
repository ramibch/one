from django.core.management.base import BaseCommand

from one.products.tasks import sync_products


class Command(BaseCommand):
    help = "Sync products"

    def handle(self, *args, **options):
        sync_products()
