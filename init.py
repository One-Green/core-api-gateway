import os
import sys
import django
from datetime import time
from django.db import connections
from django.db.utils import ProgrammingError
from django.core.management import call_command
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.insert(0, os.path.abspath("."))
django.setup()

from django.contrib.auth.models import User
from plant_core.models import PlantSettings, EnclosureSensor

call_command('makemigrations', interactive=False, verbosity=2)
call_command('makemigrations', 'plant_core', interactive=False, verbosity=2)
call_command('migrate', interactive=False, verbosity=2)
call_command('collectstatic', interactive=False, verbosity=2)

try:
    User.objects.create_superuser("plant", "change@me.com", "keeper")
except django.db.utils.IntegrityError:
    print('[WAR] User "plant" already exist')

PlantSettings(
    plant_identifier="auto_init",
    plant_type="auto_init",
    air_temperature_min=20.0,
    air_temperature_max=22.0,
    air_hygrometry_min=40,
    air_hygrometry_max=60,
    air_co2_ppm_min=3000.0,
    air_co2_ppm_max=5000.0,
    light_start=time(7, 0),
    light_end=time(20, 0),
    water_tank_min_level=20,
    activate_cooler_controller=True,
    activate_heater_controller=True,
    activate_air_humidifier_controller=True,
    activate_uv_light_controller=True,
    activate_sprinklers_controller=True,
    activate_water_controller=True
).save()

EnclosureSensor(
    temperature=0,
    humidity=0,
    uv_index=0,
    co2_ppm=0,
    cov_ppm=0
).save()
