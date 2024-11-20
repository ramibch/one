import psycopg
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a Postgres db"

    def handle(self, *args, **options):
        db_name, host, port = settings.DB_NAME, settings.DB_HOST, settings.DB_PORT
        su, su_pw = settings.DB_SUPERUSER, settings.DB_SUPERPASSWORD

        if input(f"Enter 'Drop {db_name}' to confirm: ") == f"Drop {db_name}":
            conn = f"user='{su}' password='{su_pw}' host='{host}' port='{port}'"
            with psycopg.connect(conn, autocommit=True).cursor() as cur:
                cur.execute(f"DROP DATABASE {db_name};")
            msg = f"Postgres database '{db_name}' is dropped."
            self.stdout.write(self.style.SUCCESS(msg))
        else:
            msg = f"Confirmation declied. Not dropping '{db_name}'."
            self.stdout.write(self.style.WARNING(msg))
