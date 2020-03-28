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
from core.aggregator import BaseAggregator
from plant_core.models import PlantSettings
from plant_core.models import (Enclosure,
                               Cooler)

# give a name for controlled device
# for printing / logging purpose
CONTROLLED_DEVICE: str = 'cooler'

# Print template
# generic template for logging/print (for log remove datetime_now)
PRINT_TEMPLATE = '[INFO] [{device}] ; {temperature} ; {hygrometry} ; {_action}'

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

    # Cooling decrease controller
    temperature_dec_ctl = BaseController(
        kind='CUT_OUT',
        neutral=plant_settings['air_temperature'],
        delta_max=2,
        delta_min=0
    )
    # Hygrometry decrease controller
    hygrometry_dec_ctl = BaseController(
        kind='CUT_OUT',
        neutral=plant_settings['air_hygrometry'],
        delta_max=5,
        delta_min=0
    )
    # Temperature + Hygrometry decrease are controlled by
    # one device -> peltier
    peltier_device_ctl = BaseAggregator(
        [
            temperature_dec_ctl,
            hygrometry_dec_ctl
        ]
    )

    # Read enclosure status
    status = Enclosure.get_status()
    if not status == {}:
        t = status['enclosure_temperature']
        hr = status['enclosure_hygrometry']

        # Set values to controller
        temperature_dec_ctl.set_sensor_value(t)
        hygrometry_dec_ctl.set_sensor_value(hr)

        # Get aggregated action
        action: int = peltier_device_ctl.action
        # init last_action for init
        if first_loop:
            first_loop = False
            last_action = action
            logger.info(
                PRINT_TEMPLATE.format(
                    device=CONTROLLED_DEVICE,
                    temperature=t,
                    hygrometry=hr,
                    _action=action
                )
            )
            Cooler.set_power_status(action)

        elif action != last_action:
            last_action = action
            logger.info(
                PRINT_TEMPLATE.format(
                    device=CONTROLLED_DEVICE,
                    temperature=t,
                    hygrometry=hr,
                    _action=action
                )
            )
            Cooler.set_power_status(action)


if __name__ == '__main__':
    logging.warning(
        f'[WARNING] [{CONTROLLED_DEVICE}] device debug mode, '
        f'use controller/run.py to load controller'
    )
    while True:
        main()
