import os
import sys
import time
from typing import Union
from datetime import datetime
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(os.path.dirname(os.path.dirname(os.path.join('..', '..', os.path.dirname('__file__')))))
django.setup()

from core.controller import BaseTimeController
from plant_core.models import PlantSettings
from plant_core.models import UvLight

# give a name for controlled device
# for printing / logging purpose
CONTROLLED_DEVICE: str = 'UV_LIGHT'

# Print template
# generic template for logging/print (for log remove datetime_now)
PRINT_TEMPLATE = ('{datetime_now};{device};'
                  'start_at={light_start_at};end_at={light_end_at};'
                  '{_action}')

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
PLANT_SETTINGS: dict = PlantSettings.get_settings()

start_at = PLANT_SETTINGS['light_start']
end_at = PLANT_SETTINGS['light_end']

# Create time based controller
uv_io_ctl = BaseTimeController(start_at, end_at)

first_loop: bool = True
last_action: Union[bool, None] = None


def main():
    global first_loop, last_action

    # Get action
    action: bool = uv_io_ctl.action
    # init last_action for init
    if first_loop:
        first_loop = False
        last_action = action
        print(PRINT_TEMPLATE.format(datetime_now=datetime.now(), device=CONTROLLED_DEVICE,
                                    light_start_at=start_at, light_end_at=end_at, _action=action))
        UvLight.set_power_status(action)
    elif action != last_action:
        last_action = action
        print(PRINT_TEMPLATE.format(datetime_now=datetime.now(), device=CONTROLLED_DEVICE,
                                    light_start_at=start_at, light_end_at=end_at, _action=action))
        UvLight.set_power_status(action)


if __name__ == '__main__':
    print(f'[!] Warning: {CONTROLLED_DEVICE} device debug mode, use controller/run.py to load controller')
    while True:
        main()
        time.sleep(1)
