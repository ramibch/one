from django.core.management import call_command
from django.core.management.base import BaseCommand

from ...utils.abstracts import BaseSubmodule


class Command(BaseCommand):
    help = "Seed data in the database"

    def handle(self, *args, **options):
        # Make migrations just in case
        call_command("makemigrations")

        # Create database
        call_command("createdb")

        # Migrate
        call_command("migrate")

        # Collect static
        call_command("collectstatic", interactive=False)

        # Sync submodule folders
        BaseSubmodule.sync_all_folders()

        # Create menus
        call_command("createmenus")
