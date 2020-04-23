import os
import sys
import django
from datetime import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.join(os.path.dirname("__file__"))))
)
django.setup()
from plant_core.models import PlantSettings, EnclosureSensor

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
    activate_cooler_controller=True,
    activate_heater_controller=True,
    activate_air_humidifier_controller=True,
    activate_uv_light_controller=True,
    activate_sprinklers_controller=True,
).save()

EnclosureSensor(temperature=0, humidity=0, uv_index=0, co2_ppm=0, cov_ppm=0).save()
