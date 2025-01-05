from django.core.management.base import BaseCommand
from django.db import transaction

from tex.values import LATEX_LANGUAGES

from ...listing_types.calendar import create_calendar
from ...texts import TEXT_CALENDAR


class Command(BaseCommand):
    help = "Create calendars for listings"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Processing...")
        for lang in ("en", "es", "de"):
            for year in (2024, 2025, 2026):
                context = {
                    "doc_language": LATEX_LANGUAGES[lang],
                    "title": TEXT_CALENDAR[lang],
                }
                create_calendar(lang, year, context)
                del context
        self.stdout.write("Done.")
