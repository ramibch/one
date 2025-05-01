import psycopg
from django.conf import settings
from django.core.management.base import BaseCommand
from psycopg.errors import DuplicateDatabase, DuplicateObject


class Command(BaseCommand):
    help = "Create a Postgres db"

    def handle(self, *args, **options):
        db_name: str = settings.DB_NAME
        host: str = settings.DB_HOST
        port: str = settings.DB_PORT
        su: str = settings.DB_SUPERUSER
        su_pw: str = settings.DB_SUPERPASSWORD
        u: str = settings.DB_USER
        pw: str = settings.DB_PASSWORD

        conn = f"user='{su}' password='{su_pw}' host='{host}' port='{port}'"

        with psycopg.connect(conn, autocommit=True).cursor() as cur:
            try:
                cur.execute(f"CREATE DATABASE {db_name};")
                cur.execute(f"CREATE USER {u} WITH PASSWORD '{pw}';")
            except DuplicateDatabase:
                msg = f"Database '{db_name}' already exists"
                self.stdout.write(self.style.WARNING(msg))
            except DuplicateObject:
                msg = f"User '{u}' already exists"
                self.stdout.write(self.style.WARNING(msg))

            cur.execute(f"ALTER ROLE {u} SET client_encoding TO 'utf8';")
            cur.execute(f"ALTER ROLE {u} SET timezone TO 'UTC';")
            cur.execute(
                f"ALTER ROLE {u} SET default_transaction_isolation TO 'read committed';"
            )
            cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {u};")
            cur.execute(f"ALTER USER {u} CREATEDB;")
            cur.execute(f"ALTER DATABASE {db_name} OWNER TO {u};")
