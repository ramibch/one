from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import BaseCommand

from ....utils.abstracts import AbstractSubmoduleFolderModel


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
        call_command("collectstatic")

        # Create sites
        for env in envs:
            call_command("createsites", env)

        # Create links
        call_command("createlinks")

        # Get sites

        sites = Site.objects.all()

        # Sync submodule folders
        AbstractSubmoduleFolderModel.sync_all_folders()

        # Create menus
        for env in envs:
            # TODO: continue here
            print()
            pass
            # call_command("createmenus", env)
