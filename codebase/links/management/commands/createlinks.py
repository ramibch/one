from django.core.management.base import BaseCommand

from ...models import create_initial_django_links


class Command(BaseCommand):
    help = "Creates initial links"

    def handle(self, *args, **options):
        created_links = create_initial_django_links()

        if len(created_links) > 0:
            objs_str = "\n".join(str(obj) for obj in created_links)
            self.stdout.write(
                self.style.SUCCESS(f"Links successfully created:\n{objs_str}")
            )
        else:
            self.stdout.write(self.style.WARNING("Links are already created"))
