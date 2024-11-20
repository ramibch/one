from django.core.management import call_command
from django.core.management.base import BaseCommand

from ....utils.abstracts import SubmodulesFolder


class Command(BaseCommand):
    help = "Seed data in the database"

    def add_arguments(self, parser):
        parser.add_argument("environments", nargs="+", type=str)

    def handle(self, *args, **options):
        envs = options["environments"]
        # Create database
        call_command("createdb")

        # Migrate
        call_command("migrate")

        # Collect static
        call_command("collectstatic", interactive=False)

        # Create sites
        call_command("createsites", *envs)

        # Create links
        call_command("createlinks")

        # Sync submodule folders
        SubmodulesFolder.sync_all_folders()

        # Create menus
        call_command("createmenus")
