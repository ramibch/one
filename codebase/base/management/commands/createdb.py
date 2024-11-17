import psycopg
from django.conf import settings
from django.core.management.base import BaseCommand
from psycopg.errors import DuplicateDatabase, DuplicateObject


class Command(BaseCommand):
    help = "Create a Postgres db"

    def handle(self, *args, **options):
        if not settings.USE_POSTGRES:
            self.stdout.write(self.style.WARNING("Not creating db, since Postgres is not being used."))
            return

        db_name, host, port = settings.POSTGRES_DB, settings.POSTGRES_HOST, settings.POSTGRES_PORT
        superuser, superpassword = settings.POSTGRES_SUPERUSER, settings.POSTGRES_SUPERPASSWORD
        user, pasword = settings.POSTGRES_USER, settings.POSTGRES_PASSWORD
        connection_string = f"user='{superuser}' password='{superpassword}' host='{host}' port='{port}'"

        with psycopg.connect(connection_string, autocommit=True).cursor() as cur:
            try:
                cur.execute(f"CREATE DATABASE {db_name};")
            except DuplicateDatabase:
                self.stdout.write(self.style.WARNING(f"Database '{db_name}' already exists"))

            try:
                cur.execute(f"CREATE USER {user} WITH PASSWORD '{pasword}';")
            except DuplicateObject:
                self.stdout.write(self.style.WARNING(f"User '{user}' already exists"))

            cur.execute(f"ALTER ROLE {user} SET client_encoding TO 'utf8';")
            cur.execute(f"ALTER ROLE {user} SET timezone TO 'UTC';")
            cur.execute(f"ALTER ROLE {user} SET default_transaction_isolation TO 'read committed';")
            cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {user};")
            cur.execute(f"ALTER USER {user} CREATEDB;")
            cur.execute(f"ALTER DATABASE {db_name} OWNER TO {user};")
