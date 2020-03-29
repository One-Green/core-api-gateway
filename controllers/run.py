import os
import sys
import time
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(os.path.dirname(os.path.dirname(os.path.join('..', '..', os.path.dirname('__file__')))))
django.setup()

from plant_core.models import PlantSettings
from controllers import (
    cooler,
    heater,
    air_humidifier,
    light,
    sprinklers,
    water_pump
)

# Run all controllers
while True:
    settings = PlantSettings.get_settings()

    if settings['activate_cooler_controller']:
        cooler.main()

    if settings['activate_heater_controller']:
        heater.main()

    if settings['activate_air_humidifier_controller']:
        air_humidifier.main()

    if settings['activate_uv_light_controller']:
        light.main()

    if settings['activate_soil_humidifier_controller']:
        sprinklers.main()
        water_pump.main()

    time.sleep(0.5)
