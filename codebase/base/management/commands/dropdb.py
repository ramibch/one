import psycopg
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a Postgres db"

    def handle(self, *args, **options):
        if not settings.USE_POSTGRES:
            self.stdout.write(self.style.WARNING("Postgres is not being used."))
            return

        db_name, host, port = (
            settings.POSTGRES_DB,
            settings.POSTGRES_HOST,
            settings.POSTGRES_PORT,
        )
        superuser, superpassword = (
            settings.POSTGRES_SUPERUSER,
            settings.POSTGRES_SUPERPASSWORD,
        )
        print(f"Enter 'Drop {db_name}':")
        if input() == f"Drop {db_name}":
            with psycopg.connect(
                f"user='{superuser}' password='{superpassword}' host='{host}' port='{port}'",
                autocommit=True,
            ).cursor() as cur:
                cur.execute(f"DROP DATABASE {db_name};")
            self.stdout.write(
                self.style.SUCCESS(f"Postgres database '{db_name}' is dropped.")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Confirmation declied. Not dropping '{db_name}'.")
            )
