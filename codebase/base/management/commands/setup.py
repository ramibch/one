from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from ...utils.abstracts import BaseSubmoduleFolder

User = get_user_model()


class Command(BaseCommand):
    help = "The only commands thats need to be run to get the project."

    def handle(self, *args, **options):
        # Make migrations only in development

        call_command("makemigrations")

        # Create database
        call_command("createdb")

        # Migrate
        call_command("migrate")

        # Create superuser
        if not User.objects.exists():
            call_command("createsuperuser", "--noinput")

        # Collect static
        if settings.ENV == "prod":
            call_command("collectstatic", interactive=False)

        # Sync submodule folders
        BaseSubmoduleFolder.sync_all_folders()
