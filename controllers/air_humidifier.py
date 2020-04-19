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
    AirHumidifierSensor,
    AirHumidifier

)

# give a name for controlled device
# for printing / logging purpose
CONTROLLED_DEVICE: str = 'air-humidifier'

ctl = BinaryController()


def main():
    setting = PlantSettings.get_settings()
    enclosure = EnclosureSensor.get_status()
    sensor = AirHumidifierSensor.get_status()
    if enclosure and sensor:
        ctl.set_conf(
            _min=setting.air_hygrometry_min,
            _max=setting.air_hygrometry_max,
            reverse=False
        )
        signal = ctl.get_signal(enclosure.humidity)

        AirHumidifier(
            enclosure_humidity=enclosure.humidity,
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
                f'h_enclosure={round(enclosure.humidity)} '
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
    while True:
        if PlantSettings.get_settings().activate_air_humidifier_controller:
            main()
            time.sleep(CONTROLLERS_LOOP_EVERY)
        else:
            print('[INFO] AIR HUMIDIFIER DEACTIVATED')
            time.sleep(5)
