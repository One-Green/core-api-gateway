import os
import sys
import time
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(os.path.dirname(os.path.dirname(os.path.join('..', '..', os.path.dirname('__file__')))))
django.setup()

from plant_kiper.settings import (
    controller_logger,
    CONTROLLERS_LOOP_EVERY
)
from controllers import loki_tag
from core.controller import BinaryController
from plant_core.models import (
    EnclosureSensor,
    PlantSettings,
    CoolerSensor,
    Cooler
)

CONTROLLED_DEVICE: str = 'cooler'

t_ctl = BinaryController()
h_ctl = BinaryController()


def main():
    setting = PlantSettings.get_settings()
    enclosure = EnclosureSensor.get_status()
    sensor = CoolerSensor.get_status()
    if enclosure and sensor:
        t_ctl.set_conf(
            _min=setting.air_temperature_min,
            _max=setting.air_temperature_max,
            reverse=True
        )
        t_signal = t_ctl.get_signal(enclosure.temperature)

        h_ctl.set_conf(
            _min=setting.air_hygrometry_min,
            _max=setting.air_hygrometry_max,
            reverse=True
        )
        h_signal = h_ctl.get_signal(enclosure.humidity)

        Cooler(
            enclosure_temperature=enclosure.temperature,
            enclosure_humidity=enclosure.humidity,
            temperature_in=sensor.air_in_temperature,
            humidity_in=sensor.air_in_humidity,
            temperature_level_min=setting.air_temperature_min,
            temperature_level_max=setting.air_temperature_max,
            humidity_level_min=setting.air_hygrometry_min,
            humidity_level_max=setting.air_hygrometry_max,
            power_temperature=t_signal,
            power_humidity=h_signal
        ).save()
        controller_logger.info(
            (
                f'[INFO] [{CONTROLLED_DEVICE}] '
                f't_min={round(setting.air_temperature_min)}, '
                f't_max={round(setting.air_temperature_max)} '
                f't_enclosure={round(enclosure.humidity)} '
                f"action={t_signal}"
            ),
            extra={
                "tags": {
                    "controller": CONTROLLED_DEVICE,
                    "which-request": "temperature",
                }
            }

        )

        controller_logger.info(
            (
                f'[INFO] [{CONTROLLED_DEVICE}] '
                f'h_min={round(setting.air_hygrometry_min)}, '
                f'h_max={round(setting.air_hygrometry_max)} '
                f'h_enclosure={round(enclosure.humidity)} '
                f"action={h_signal}"
            ),
            extra={
                "tags": {
                    "controller": CONTROLLED_DEVICE,
                    "which-request": "humidity",
                }
            }

        )
    else:
        Cooler(
            power_temperature=0,
            power_humidity=0
        ).save()
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
    while True:
        if PlantSettings.get_settings().activate_cooler_controller:
            main()
            time.sleep(CONTROLLERS_LOOP_EVERY)
        else:
            print('[INFO] COOLER DEACTIVATED')
            time.sleep(5)
