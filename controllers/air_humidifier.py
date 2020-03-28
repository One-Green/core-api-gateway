import os
import sys
from typing import Union
from datetime import datetime
import django
import logging
import logging_loki

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(os.path.dirname(os.path.dirname(os.path.join('..', '..', os.path.dirname('__file__')))))
django.setup()

from core.controller import BaseController
from plant_core.models import PlantSettings
from plant_core.models import (Enclosure,
                               AirHumidifier)

# give a name for controlled device
# for printing / logging purpose
CONTROLLED_DEVICE: str = 'air-humidifier'

# Print template
# generic template for logging/print (for log remove datetime_now)
PRINT_TEMPLATE = '[INFO] [{device}] ; {hygrometry} ; {_action}'

# Stream to logs to Loki + Stdout
logger = logging.getLogger(f'controllers-logger')
logger.addHandler(
    logging_loki.LokiHandler(
        url="http://loki:3100/loki/api/v1/push",
        tags={"controller": CONTROLLED_DEVICE},
        version="1",
    )
)
logger.addHandler(
    logging.StreamHandler()
)
logger.setLevel(logging.DEBUG)

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
    hygrometry_inc_ctl = BaseController(
        kind='CUT_OUT',
        neutral=plant_settings['air_hygrometry'],
        delta_max=0,
        delta_min=5,
        reverse=True
    )

    # Read enclosure status
    status = Enclosure.get_status()
    # Read Vapor generator water level
    vapor_gen_status = AirHumidifier.get_status()

    if not status == {}:
        hr = status['enclosure_hygrometry']
        # Set values to controller
        hygrometry_inc_ctl.set_sensor_value(hr)
        # Get action
        action: int = hygrometry_inc_ctl.action

        try:
            _water_level = vapor_gen_status['water_level']
        except KeyError:
            _water_level = None

        if not _water_level:
            _water_level = 0.
            logger.error(
                f'[ERROR] [{CONTROLLED_DEVICE}] '
                f'status or vapor_gen_status '
                f'is empty ... water level is working ??',
                extra={"tags": {"service": "my-service"}},
            )
            logger.warning(f'[WARNING] [{CONTROLLED_DEVICE}] water level set == 0.0')

        if _water_level < min_water_level:
            logger.info(
                PRINT_TEMPLATE.format(
                    device=CONTROLLED_DEVICE,
                    hygrometry=hr,
                    _action='water level to low , fill water tank')
            )
        # init last_action for init
        if first_loop:
            first_loop = False
            last_action = action
            logger.info(
                PRINT_TEMPLATE.format(
                    device=CONTROLLED_DEVICE,
                    hygrometry=hr,
                    _action=action)
            )
            AirHumidifier.set_power_status(action)

        elif action != last_action:
            last_action = action
            logger.info(
                PRINT_TEMPLATE.format(
                    datetime_now=datetime.now(),
                    device=CONTROLLED_DEVICE,
                    hygrometry=hr,
                    _action=action)
            )
            AirHumidifier.set_power_status(action)


if __name__ == '__main__':
    logger.warning(
        f'[WARNING] [{CONTROLLED_DEVICE}] device debug mode, '
        f'use controller/run.py to load controller'
    )
    while True:
        main()
