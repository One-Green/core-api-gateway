import os
import sys
import django
import psycopg2
from django.core.management import call_command
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
sys.path.insert(0, os.path.abspath("."))
django.setup()

POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

con = psycopg2.connect(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database="postgres",
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
)

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = con.cursor()
try:
    cursor.execute(f"create database {POSTGRES_DB};")
    print(f"[OK] Database {POSTGRES_DB} created")
except psycopg2.errors.DuplicateDatabase:
    print(f"[OK] Database {POSTGRES_DB} already exist")

print("[INFO] Executing django db migrations ...")
call_command("makemigrations", interactive=False, verbosity=2)
call_command("makemigrations", "glbl", interactive=False, verbosity=2)
call_command("makemigrations", "sprinkler", interactive=False, verbosity=2)
call_command("makemigrations", "water", interactive=False, verbosity=2)
call_command("makemigrations", "light", interactive=False, verbosity=2)
call_command("migrate", interactive=False, verbosity=2)
