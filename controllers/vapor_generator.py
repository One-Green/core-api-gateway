import os
import sys
import time
from typing import Union
from datetime import datetime
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(os.path.dirname(os.path.dirname(os.path.join('..', '..', os.path.dirname('__file__')))))
django.setup()

from core.controller import BaseController
from plant_core.models import PlantSettings
from plant_core.models import (Enclosure,
                               VaporGenerator)

# give a name for controlled device
# for printing / logging purpose
CONTROLLED_DEVICE: str = 'VAPOR_GENERATOR'

# Print template
# generic template for logging/print (for log remove datetime_now)
PRINT_TEMPLATE = '{datetime_now};{device};{hygrometry};{_action}'

first_loop: bool = True
last_action: Union[int, None] = None


def main():
    global first_loop, last_action

    # Water level alert
    # suppose value in percent
    min_water_level: float = 20.

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
    plant_settings: dict = PlantSettings.get_settings()

    # Heater increase controller
    hygrometry_inc_ctl = BaseController(kind='CUT_OUT',
                                        neutral=plant_settings['air_hygrometry'],
                                        delta_max=0,
                                        delta_min=5,
                                        reverse=True)

    # Read enclosure status
    status = Enclosure.get_status()
    # Read Vapor generator water level
    vapor_gen_status = VaporGenerator.get_status()

    if not status == {} and not vapor_gen_status == {}:
        print(f'[!] Warning: {CONTROLLED_DEVICE} status or vapor_gen_status is empty ... water level is working ??')
        hr = status['enclosure_hygrometry']
        _water_level = vapor_gen_status['water_level']

        # Set values to controller
        hygrometry_inc_ctl.set_sensor_value(hr)
        # Get action
        action: bool = hygrometry_inc_ctl.action

        if _water_level < min_water_level:
            print(PRINT_TEMPLATE.format(datetime_now=datetime.now(), device=CONTROLLED_DEVICE,
                                        hygrometry=hr, _action='[!] Water level to low , fill water tank'))
        # init last_action for init
        elif first_loop:
            first_loop = False
            last_action = action
            print(PRINT_TEMPLATE.format(datetime_now=datetime.now(), device=CONTROLLED_DEVICE,
                                        hygrometry=hr, _action=action))
            VaporGenerator.set_power_status(action)

        elif action != last_action:
            last_action = action
            print(PRINT_TEMPLATE.format(datetime_now=datetime.now(), device=CONTROLLED_DEVICE,
                                        hygrometry=hr, _action=action))
            VaporGenerator.set_power_status(action)


if __name__ == '__main__':
    print(f'[!] Warning: {CONTROLLED_DEVICE} device debug mode, use controller/run.py to load controller')
    while True:
        main()
        time.sleep(1)
