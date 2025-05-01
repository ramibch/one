import psycopg
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Drop a Postgres db"

    def handle(self, *args, **options):
        db_name: str = settings.DB_NAME
        host: str = settings.DB_HOST
        port: str = settings.DB_PORT
        su: str = settings.DB_SUPERUSER
        su_pw: str = settings.DB_SUPERPASSWORD

        if input(f"Enter 'Drop {db_name}' to confirm: ") == f"Drop {db_name}":
            conn = f"user='{su}' password='{su_pw}' host='{host}' port='{port}'"
            with psycopg.connect(conn, autocommit=True).cursor() as cur:
                cur.execute(f"DROP DATABASE {db_name};")
                msg = f"Postgres database '{db_name}' is dropped."
                self.stdout.write(self.style.SUCCESS(msg))
        else:
            msg = f"Confirmation declied. Not dropping '{db_name}'."
            self.stdout.write(self.style.WARNING(msg))
