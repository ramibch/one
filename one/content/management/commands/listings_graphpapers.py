from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import translation

from ...listing_types.graphpaper import PATTERNS, create_graphpaper


class Command(BaseCommand):
    help = "Create graph paper Listings"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Processing...")
        for lang in settings.LANGUAGE_CODES:
            with translation.override(lang):
                for pattern_key in PATTERNS.keys():
                    create_graphpaper(pattern_key)
                    print(f"✔ {pattern_key} {lang}")
        self.stdout.write("Done.")
