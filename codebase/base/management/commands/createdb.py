import sys

import psycopg
from django.conf import settings
from django.core.management.base import BaseCommand
from psycopg.errors import DuplicateDatabase, DuplicateObject


class Command(BaseCommand):
    help = "Create a Postgres db"

    def handle(self, *args, **options):
        db_name, host, port = settings.DB_NAME, settings.DB_HOST, settings.DB_PORT
        su, su_pw = settings.DB_SUPERUSER, settings.DB_SUPERPASSWORD
        u, pw = settings.DB_USER, settings.DB_PASSWORD

        conn = f"user='{su}' password='{su_pw}' host='{host}' port='{port}'"

        with psycopg.connect(conn, autocommit=True).cursor() as cur:
            try:
                cur.execute(f"CREATE DATABASE {db_name};")
            except DuplicateDatabase:
                msg = f"Database '{db_name}' already exists"
                self.stdout.write(self.style.WARNING(msg))
                cur.close()
                sys.exit(1)

            try:
                cur.execute(f"CREATE USER {u} WITH PASSWORD '{pw}';")
            except DuplicateObject:
                self.stdout.write(self.style.WARNING(f"User '{u}' already exists"))

            cur.execute(f"ALTER ROLE {u} SET client_encoding TO 'utf8';")
            cur.execute(f"ALTER ROLE {u} SET timezone TO 'UTC';")
            cur.execute(
                f"ALTER ROLE {u} SET default_transaction_isolation TO 'read committed';"
            )
            cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {u};")
            cur.execute(f"ALTER USER {u} CREATEDB;")
            cur.execute(f"ALTER DATABASE {db_name} OWNER TO {u};")
