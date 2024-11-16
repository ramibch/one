from django.core.management.base import BaseCommand

from ...models import create_initial_django_links


class Command(BaseCommand):
    help = "Creates initial links"

    def handle(self, *args, **options):
        objs_str = "\n".join(str(obj) for obj in create_initial_django_links())
        self.stdout.write(self.style.SUCCESS(f"Links successfully created:\n{objs_str}"))
