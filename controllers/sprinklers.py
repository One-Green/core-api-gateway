import os
import sys
from typing import Union
import django
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(os.path.dirname(os.path.dirname(os.path.join('..', '..', os.path.dirname('__file__')))))
django.setup()

from plant_kiper.settings import controller_logger
from core.controller import BaseController
from plant_core.models import (
    SprinklerTag,
    SprinklerSettings,
    SprinklerValve,
    WaterPump
)

# give a name for controlled device
# for printing / logging purpose
CONTROLLED_DEVICE: str = 'sprinklers'

# Print template
# generic template for logging/print (for log remove datetime_now)
PRINT_TEMPLATE = (
    '[INFO] [{device}] ; tag={tag} ; '
    'humidity setting = {setting} ; '
    'humidity sensor  = {humidity} ; '
    'controller action = {action}'
)

first_loop: bool = True
last_action: Union[int, None] = None


def main():
    global first_loop, last_action

    for tag in SprinklerTag.objects.all():
        print(f'processing tag = {tag.tag}')
        setting = SprinklerSettings.objects.get(tag=tag)
        status = SprinklerValve.get_status(tag)

        ctl = BaseController(
            kind='CUT_OUT',
            neutral=setting.soil_hygrometry,
            delta_max=10,
            delta_min=10,
            reverse=True
        )

        if status:
            ctl.set_sensor_value(
                status.soil_hygrometry
            )
            action = ctl.action

        if status and first_loop:
            first_loop = False
            last_action = action

        if (
                status
                and action != last_action
        ):
            SprinklerValve.set_power_status(tag, action)
            WaterPump.set_power_status(action)
            last_action = action


if __name__ == '__main__':
    print(
        f'[WARNING] [{CONTROLLED_DEVICE}] device debug mode, '
        f'use controller/run.py to load controller'
    )
    while True:
        main()
        time.sleep(1)
