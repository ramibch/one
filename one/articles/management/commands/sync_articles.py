from django.core.management.base import BaseCommand

from ....articles.tasks import sync_articles


class Command(BaseCommand):
    help = "Sync articles"

    def handle(self, *args, **options):
        sync_articles()
