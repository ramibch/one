from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Language


class Command(BaseCommand):
    help = "Creates languages in db that are defined in the setting"

    def handle(self, *args, **options):
        langs = []
        for code, _ in settings.LANGUAGES:
            langs.append(Language(id=code))
        Language.objects.bulk_create(
            langs,
            unique_fields=["id"],
            update_fields=["id"],
            ignore_conflicts=True,
        )
