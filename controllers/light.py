import os
import sys
from typing import Union
from datetime import datetime
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(os.path.dirname(os.path.dirname(os.path.join('..', '..', os.path.dirname('__file__')))))
django.setup()

from plant_kiper.settings import controller_logger
from core.controller import BaseTimeRangeController
from plant_core.models import PlantSettings
from plant_core.models import UvLight

# give a name for controlled device
# for printing / logging purpose
CONTROLLED_DEVICE: str = 'uv-light'

# Print template
# generic template for logging/print (for log remove datetime_now)
PRINT_TEMPLATE = ('[INFO] [{device}] ; '
                  'start_at={light_start_at} ; '
                  'end_at={light_end_at} ; '
                  '{_action}')

first_loop: bool = True
last_action: Union[int, None] = None


def main():
    global first_loop, last_action

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

    start_at = plant_settings['light_start']
    end_at = plant_settings['light_end']

    # Create time based controller
    uv_io_ctl = BaseTimeRangeController(
        start_at,
        end_at
    )

    # set current time
    uv_io_ctl.set_current_time(datetime.now().time())
    # Get action
    action: int = uv_io_ctl.action
    # init last_action for init
    if first_loop:
        first_loop = False
        last_action = action
        controller_logger.info(
            PRINT_TEMPLATE.format(
                device=CONTROLLED_DEVICE,
                light_start_at=start_at,
                light_end_at=end_at,
                _action=action
            ),
            extra={"tags": {"controller": CONTROLLED_DEVICE}}
        )
        UvLight.set_power_status(action)
    elif action != last_action:
        last_action = action
        controller_logger.info(
            PRINT_TEMPLATE.format(
                device=CONTROLLED_DEVICE,
                light_start_at=start_at,
                light_end_at=end_at,
                _action=action
            ),
            extra={"tags": {"controller": CONTROLLED_DEVICE}}
        )
        UvLight.set_power_status(action)


if __name__ == '__main__':
    controller_logger.warning(
        f'[WARNING] [{CONTROLLED_DEVICE}] device debug mode, '
        f'use controller/run.py to load controller',
        extra={"tags": {"controller": CONTROLLED_DEVICE}}
    )
    while True:
        main()
