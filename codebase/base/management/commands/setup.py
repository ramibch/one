from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from ...utils.abstracts import BaseSubmodule


class Command(BaseCommand):
    help = "The only commands thats need to be run to get the project."

    def handle(self, *args, **options):
        # Make migrations only in development
        if settings.ENV == "dev":
            call_command("makemigrations")

        # Create database
        call_command("createdb")

        # Migrate
        call_command("migrate")

        # Collect static
        if settings.ENV != "dev":
            call_command("collectstatic", interactive=False)

        # Sync submodule folders
        BaseSubmodule.sync_all_folders()
