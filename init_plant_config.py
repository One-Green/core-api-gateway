import os
import sys
import django
from datetime import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(os.path.dirname(os.path.dirname(os.path.join(os.path.dirname('__file__')))))
django.setup()
from plant_core.models import PlantSettings

PlantSettings(
    plant_identifier='auto_init',
    plant_type='auto_init',
    air_temperature=20.,
    air_hygrometry=50,
    air_co2_ppm=5000.,
    soil_hygrometry=50.,
    light_start=time(7, 0),
    light_end=time(20, 0),
    activate_cooler_controller=True,
    activate_heater_controller=True,
    activate_air_humidifier_controller=True,
    activate_uv_light_controller=True,
    activate_soil_humidifier_controller=True
).save()
