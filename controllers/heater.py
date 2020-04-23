import os
import sys
import time
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.join("..", "..", os.path.dirname("__file__")))
    )
)
django.setup()

from plant_kiper.settings import controller_logger, CONTROLLERS_LOOP_EVERY
from controllers import loki_tag
from core.controller import BinaryController
from core.utils import is_api_gateway_up
from plant_core.models import EnclosureSensor, PlantSettings, HeaterSensor, Heater

while not is_api_gateway_up():
    time.sleep(30)

# give a name for controlled device
# for printing / logging purpose
CONTROLLED_DEVICE: str = "heater"

ctl = BinaryController()


def main():
    setting = PlantSettings.get_settings()
    enclosure = EnclosureSensor.get_status()
    sensor = HeaterSensor.get_status()
    if enclosure and sensor:
        ctl.set_conf(
            _min=setting.air_temperature_min,
            _max=setting.air_temperature_max,
            reverse=False,
        )
        signal = ctl.get_signal(enclosure.temperature)

        Heater(
            enclosure_temperature=enclosure.temperature,
            temperature_in=sensor.air_in_temperature,
            temperature_level_min=setting.air_temperature_min,
            temperature_level_max=setting.air_temperature_max,
            power=signal,
        ).save()
        controller_logger.info(
            (
                f"[INFO] [{CONTROLLED_DEVICE}] "
                f"t_min={round(setting.air_temperature_min)}, "
                f"t_max={round(setting.air_temperature_max)} "
                f"t_enclosure={round(enclosure.temperature)} "
                f"action={signal}"
            ),
            extra={"tags": {"controller": CONTROLLED_DEVICE}},
        )

    else:
        Heater(power=0).save()
        controller_logger.error(
            (
                f"[ERROR] [{CONTROLLED_DEVICE}] "
                f"SENSORS NO UPDATED "
                f" => POWER = OFF"
            ),
            extra={
                "tags": {
                    "controller": CONTROLLED_DEVICE,
                    "message": loki_tag.SENSOR_NOT_UPDATED,
                }
            },
        )


if __name__ == "__main__":
    while True:
        if PlantSettings.get_settings().activate_heater_controller:
            main()
            time.sleep(CONTROLLERS_LOOP_EVERY)
        else:
            print("[INFO] HEATER DEACTIVATED")
            time.sleep(5)
