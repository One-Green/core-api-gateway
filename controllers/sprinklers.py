import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(os.path.dirname(os.path.dirname(os.path.join('..', '..', os.path.dirname('__file__')))))
django.setup()

from plant_kiper.settings import controller_logger
from controllers import loki_tag
from core.controller import BinaryController
from plant_core.models import (
    SprinklerValve,
    SprinklerSettings,
    SprinklerTag,
    SprinklerSoilHumiditySensor,
)

# give a name for controlled device
# for printing / logging purpose
CONTROLLED_DEVICE: str = 'sprinklers'

# Print template
# generic template for logging/print (for log remove datetime_now)
PRINT_TEMPLATE = (
    '[INFO] [{device}] [tag={tag}] '
    'humidity min = {min} '
    'humidity max = {max} '
    'humidity sensor = {humidity} '
    'controller action = {action}'
)

ctl = BinaryController()


def main():
    for tag in SprinklerTag.objects.all():
        try:
            setting = SprinklerSettings.objects.get(tag=tag)
        except SprinklerSettings.DoesNotExist:
            controller_logger.error(
                (
                    f'[ERROR] [{CONTROLLED_DEVICE}] '
                    f'[tag={tag.tag}] '
                    f'No setting for this sprinkler '
                    f' => POWER = OFF'
                ),
                extra={
                    "tags": {
                        "controller": CONTROLLED_DEVICE,
                        'sprinkler-tag': tag.tag,
                        'message': loki_tag.SETTING_NOT_FOUND
                    }
                }
            )
            SprinklerValve(
                tag=tag,
                power=0
            ).save()
            continue

        sensor = SprinklerSoilHumiditySensor.status(tag=tag)
        if sensor:
            ctl.set_conf(
                _min=setting.soil_humidity_min,
                _max=setting.soil_humidity_max,
                reverse=False
            )
            signal = ctl.get_signal(sensor.soil_humidity)

            SprinklerValve(
                tag=tag,
                humidity_level=sensor.soil_humidity,
                humidity_level_max=setting.soil_humidity_max,
                humidity_level_min=setting.soil_humidity_min,
                power=signal,
            ).save()

            controller_logger.info(
                (
                    PRINT_TEMPLATE.format(
                        device=CONTROLLED_DEVICE,
                        tag=tag.tag,
                        min=setting.soil_humidity_min,
                        max=setting.soil_humidity_max,
                        humidity=sensor.soil_humidity,
                        action=signal
                    )
                ),
                extra={
                    "tags": {
                        "controller": CONTROLLED_DEVICE,
                        'sprinkler-tag': tag.tag,
                        'message': loki_tag.SENSOR_NOT_UPDATED
                    }
                }
            )

        else:
            SprinklerValve(
                tag=tag,
                power=0
            ).save()
            controller_logger.error(
                (
                    f'[ERROR] [{CONTROLLED_DEVICE}] '
                    f'[tag={tag.tag}] '
                    f'Soil humidity SENSORS NO UPDATED '
                    f' => POWER = OFF'
                ),
                extra={
                    "tags": {
                        "controller": CONTROLLED_DEVICE,
                        'sprinkler-tag': tag.tag,
                        'message': loki_tag.SENSOR_NOT_UPDATED
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
