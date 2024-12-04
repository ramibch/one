from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Fake data"

    def handle(self, *args, **options):
        pass
        # ArticleFactory.bulk
