from django.core.management.base import BaseCommand

from ...models import DJANGO_URL_PATHS, Link


class Command(BaseCommand):
    help = "Creates initial links"

    def handle(self, *args, **options):
        links = []
        for url_path, _ in DJANGO_URL_PATHS:
            if Link.objects.filter(django_url_path=url_path).exists():
                continue
            links.append(Link(django_url_path=url_path))

        Link.objects.bulk_create(links)
