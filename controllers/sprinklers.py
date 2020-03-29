import os
import sys
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
    SprinklerValve
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


def main():
    """
    List all tags
    Try to get configuration
    Get current status
    """

    for tag in SprinklerTag.objects.all():
        print(f'processing tag = {tag.tag}')
        try:
            setting = SprinklerSettings.objects.get(tag=tag)
            status = SprinklerValve.get_status(tag)
            if status:
                ctl = BaseController(
                    kind='CUT_OUT',
                    neutral=setting.soil_hygrometry,
                    delta_max=10,
                    delta_min=10,
                    reverse=True
                )
                ctl.set_sensor_value(status.soil_hygrometry)
                SprinklerValve.set_power_status(tag, ctl.action)

                #controller_logger.info(
                print(PRINT_TEMPLATE.format(
                        device=CONTROLLED_DEVICE,
                        tag=tag.tag,
                        setting=setting.soil_hygrometry,
                        humidity=status.soil_hygrometry,
                        action=ctl.action
                    )
                )
                #     ,
                #     extra={
                #         "tags": {
                #             "controller": CONTROLLED_DEVICE,
                #             'sprinkler-tag': tag.tag
                #         }
                #     }
                # )

        except SprinklerSettings.DoesNotExist:
            print(f'ERROR SPRINKLER SETTING NOT DEFINED for tag={tag.tag}')
            continue


if __name__ == '__main__':
    print(
        f'[WARNING] [{CONTROLLED_DEVICE}] device debug mode, '
        f'use controller/run.py to load controller'
    )
    while True:
        main()
        time.sleep(1)
