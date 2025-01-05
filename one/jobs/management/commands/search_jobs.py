import random

from django.core.management.base import BaseCommand

from jobs.models import RockenJob, create_applications


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        self.stdout.write("Searching...")
        RockenJob.search_and_create()
        self.stdout.write("Creating applications...")
        create_applications()
        self.stdout.write("Search performed and applications created")
