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
    PlantSettings,
    AirHumidifierSensor,
    AirHumidifier

)

# give a name for controlled device
# for printing / logging purpose
CONTROLLED_DEVICE: str = 'heater'

ctl = BinaryController()


def main():
    setting = PlantSettings.get_settings()
    sensor = AirHumidifierSensor.get_status()
    if sensor:
        ctl.set_conf(
            _min=setting.air_hygrometry_min,
            _max=setting.air_hygrometry_max,
            reverse=False
        )
        signal = ctl.get_signal(sensor.air_in_humidity)

        AirHumidifier(
            humidity_in=sensor.air_in_humidity,
            humidity_level_min=setting.air_hygrometry_min,
            humidity_level_max=setting.air_hygrometry_max,
            power=signal,
        ).save()
        controller_logger.info(
            (
                f'[INFO] [{CONTROLLED_DEVICE}] '
                f'h_min={round(setting.air_hygrometry_min)}, '
                f'h_max={round(setting.air_hygrometry_max)} '
                f'h_in={round(sensor.air_in_humidity)} '
                f"action={signal}"
            ),
            extra={
                "tags": {
                    "controller": CONTROLLED_DEVICE
                }
            }
        )

    else:
        AirHumidifier(power=0).save()
        controller_logger.error(
            (
                f'[ERROR] [{CONTROLLED_DEVICE}] '
                f'SENSORS NO UPDATED '
                f' => POWER = OFF'
            ),
            extra={
                "tags": {
                    "controller": CONTROLLED_DEVICE,
                    'message': loki_tag.SENSOR_NOT_UPDATED
                }
            }
        )


if __name__ == '__main__':
    controller_logger.warning(
        f'[WARNING] [{CONTROLLED_DEVICE}] device debug mode, '
        f'use controller/run.py to load controller',
        extra={"tags": {"controller": CONTROLLED_DEVICE}}
    )
    while True:
        main()
