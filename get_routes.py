import os
import sys
import django
from pprint import pprint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
sys.path.insert(0, os.path.abspath("."))
django.setup()

from light.urls import router as light_routes
from sprinkler.urls import router as sprinkler_routes

print("LIGHT ----- ")
pprint(light_routes.urls)
print("SPRINKLER ----- ")
pprint(sprinkler_routes.urls)
