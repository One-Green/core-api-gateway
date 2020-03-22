import os
import sys
import django
from controllers import cooler, heater, air_humidifier, light

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(os.path.dirname(os.path.dirname(os.path.join('..', '..', os.path.dirname('__file__')))))
django.setup()

from plant_core.models import PlantSettings


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
        # TODO add soil humidifier controller here
        pass

