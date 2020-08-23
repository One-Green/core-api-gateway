import os
import sys
import django
from django.core.management import call_command
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
sys.path.insert(0, os.path.abspath("."))
django.setup()

call_command('makemigrations', interactive=False, verbosity=2)
call_command('makemigrations', 'sprinkler', interactive=False, verbosity=2)
call_command('makemigrations', 'water', interactive=False, verbosity=2)
call_command('migrate', interactive=False, verbosity=2)
