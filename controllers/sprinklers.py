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

    # Loop in Sprinklertag model
    #   try to get setting for this specific sprinkler for controller
    #   if setting not found, broadcast POWER OFF
    #   if setting found:
    #       if sensors value in SpirnklerValve
    #           create controller
    #           set settings
    #           set sensors values
    #           get action
    #           broadcast action to take
    #       else
    #           broadcast POWER OFF
    #           Note: that suppose device not posting
    #                 sensors value to api-gateway
    for tag in SprinklerTag.objects.all():
        try:
            setting = SprinklerSettings.objects.get(tag=tag)
        except SprinklerSettings.DoesNotExist:
            SprinklerValve.set_power_status(tag, 0)
            controller_logger.error(
                (
                    f'[ERROR] [{CONTROLLED_DEVICE}] '
                    f'[tag={tag.tag} '
                    f'Soil hygrometry settings '
                    f'not done => device action = 0'
                )
                ,
                extra={
                    "tags": {
                        "controller": CONTROLLED_DEVICE,
                        'sprinkler-tag': tag.tag
                    }
                }
            )
            continue
        else:
            sensor = SprinklerValve.get_status(tag)
            if sensor['soil_hygrometry']:
                ctl = BaseController(
                    kind='CUT_OUT',
                    neutral=setting.soil_hygrometry,
                    delta_max=10,
                    delta_min=10,
                    reverse=True
                )
                ctl.set_sensor_value(sensor['soil_hygrometry'])
                SprinklerValve.set_power_status(tag, ctl.action)

                controller_logger.info(
                    PRINT_TEMPLATE.format(
                        device=CONTROLLED_DEVICE,
                        tag=tag.tag,
                        setting=setting.soil_hygrometry,
                        humidity=sensor['soil_hygrometry'],
                        action=ctl.action
                    )
                    ,
                    extra={
                        "tags": {
                            "controller": CONTROLLED_DEVICE,
                            'sprinkler-tag': tag.tag
                        }
                    }
                )
            else:
                SprinklerValve.set_power_status(tag, 0)
                controller_logger.error(
                    (
                        f'[ERROR] [{CONTROLLED_DEVICE}] '
                        f'[tag={tag.tag} '
                        f'Soil humidity SENSORS NO UPDATED '
                        f'not done => device action = 0'
                    )
                    ,
                    extra={
                        "tags": {
                            "controller": CONTROLLED_DEVICE,
                            'sprinkler-tag': tag.tag
                        }
                    }
                )


if __name__ == '__main__':
    print(
        f'[WARNING] [{CONTROLLED_DEVICE}] device debug mode, '
        f'use controller/run.py to load controller'
    )
    while True:
        main()
        time.sleep(1)
