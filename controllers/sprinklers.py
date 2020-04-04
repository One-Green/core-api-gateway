import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(os.path.dirname(os.path.dirname(os.path.join('..', '..', os.path.dirname('__file__')))))
django.setup()

from plant_kiper.settings import controller_logger
from controllers import loki_tag
from core.controller import BaseController
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
    '[INFO] [{device}] ; tag={tag} ; '
    'humidity min = {min} ; '
    'humidity max = {max} ; '
    'humidity sensor  = {humidity} ; '
    'controller action = {action}'
)


def main():
    for tag in SprinklerTag.objects.all():
        try:
            setting = SprinklerSettings.objects.get(tag=tag)
        except SprinklerSettings.DoesNotExist:
            print('no setting for this tag set power=False')
            SprinklerValve(
                tag=tag,
                power=False
            ).save()
            continue

        sensor = SprinklerSoilHumiditySensor.status(tag=tag)
        if sensor:
            ctl = BaseController(
                kind='CUT_OUT',
                neutral=setting.soil_humidity_min,
                delta_max=setting.soil_humidity_max + 5,
                delta_min=setting.soil_humidity_min - 5,
                reverse=True
            )
            ctl.set_sensor_value(
                sensor.soil_humidity
            )
            SprinklerValve(
                tag=tag,
                power=ctl.action
            )
            controller_logger.info(
                (
                    PRINT_TEMPLATE.format(
                        device=CONTROLLED_DEVICE,
                        min=setting.soil_humidity_min,
                        max=setting.soil_humidity_max,
                        humidity=sensor.soil_humidity,
                        action=ctl.action
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
                power=False
            ).save()
            controller_logger.error(
                (
                    f'[ERROR] [{CONTROLLED_DEVICE}] '
                    f'[tag={tag.tag} '
                    f'Soil humidity SENSORS NO UPDATED '
                    f'not done => POWER = OFF'
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
        controller_logger.warning(
            (
                f'[WARNING] [{CONTROLLED_DEVICE}] '
                f'tag not found'
            ),
            extra={
                "tags": {
                    "controller": CONTROLLED_DEVICE,
                    'message': loki_tag.SENSOR_NOT_UPDATED
                }
            }
        )
