import os
import sys
import time
import django
from pprint import pprint
from typing import Union

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.join("..", "..", os.path.dirname("__file__")))
    )
)
django.setup()

from core.controller import BaseController
from core.aggregator import BaseAggregator
from plant_core.models import PlantSettings
from plant_core.models import (
    Enclosure,
    CoolerController,
    AirHumidifierController,
    WaterPumpController,
    AirHumidifierController,
    UvLight,
    CO2Valve,
    Filters,
)

# Example of configuration dict returned
# by PlantSettings.get_settings()
# {'id': x,
# 'plant_identifier': 'my bansaï ficus',
# 'plant_type': 'ficus',
# 'air_temperature': 22.0,
# 'air_hygrometry': 50.0,
# 'air_co2_ppm': 5500.0,
# 'soil_hygrometry': 52.0,
# 'light_start': datetime.time(19, 10),
# 'light_end': datetime.time(19, 30)}
PLANT_SETTINGS = PlantSettings.get_settings()

# Cooling decrease controller
temperature_dec_ctl = BaseController(
    kind="CUT_OUT", neutral=PLANT_SETTINGS["air_temperature"], delta_max=2, delta_min=0
)
# Hygrometry decrease controller
hygrometry_dec_ctl = BaseController(
    kind="CUT_OUT", neutral=PLANT_SETTINGS["air_hygrometry"], delta_max=5, delta_min=0
)
# Temperature + Hygrometry decrease are controlled by
# one device -> peltier
peltier_device_ctl = BaseAggregator([temperature_dec_ctl, hygrometry_dec_ctl])

while True:
    # Read enclosure status
    enclosure_status = Enclosure.get_status()
    t = enclosure_status["enclosure_temperature"]
    hr = enclosure_status["enclosure_hygrometry"]

    # Set values to controller
    temperature_dec_ctl.set_sensor_value(t)
    hygrometry_dec_ctl.set_sensor_value(hr)

    # Get aggregated action
    action = peltier_device_ctl.action
    print(f"T={t}, HR={hr} => Peltier status = {action}")
    CoolerController(power_status=action).save()
    time.sleep(1)
