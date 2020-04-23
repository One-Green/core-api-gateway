import os
import sys
import time
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.insert(0, os.path.abspath('..'))
django.setup()

from plant_kiper.settings import controller_logger, CONTROLLERS_LOOP_EVERY
from controllers import loki_tag
from core.controller import BinaryController
from core.utils import is_api_gateway_up
from plant_core.models import (
    PlantSettings,
    SprinklerValve,
    SprinklerSettings,
    SprinklerTag,
    SprinklerSoilHumiditySensor,
)

while not is_api_gateway_up():
    time.sleep(30)

# give a name for controlled device
# for printing / logging purpose
CONTROLLED_DEVICE: str = "sprinklers"

# Print template
# generic template for logging/print (for log remove datetime_now)
PRINT_TEMPLATE = (
    "[INFO] [{device}] [tag={tag}] "
    "humidity min = {min} "
    "humidity max = {max} "
    "humidity sensor = {humidity} "
    "controller action = {action}"
)

ctl = BinaryController()


def main():
    for tag in SprinklerTag.objects.all():
        try:
            setting = SprinklerSettings.objects.get(tag=tag)
        except SprinklerSettings.DoesNotExist:
            controller_logger.error(
                (
                    f"[ERROR] [{CONTROLLED_DEVICE}] "
                    f"[tag={tag.tag}] "
                    f"No setting for this sprinkler "
                    f" => POWER = OFF"
                ),
                extra={
                    "tags": {
                        "controller": CONTROLLED_DEVICE,
                        "sprinkler-tag": tag.tag,
                        "message": loki_tag.SETTING_NOT_FOUND,
                    }
                },
            )
            SprinklerValve(tag=tag, power=0).save()
            continue

        sensor = SprinklerSoilHumiditySensor.status(tag=tag)
        if sensor:
            ctl.set_conf(
                _min=setting.soil_humidity_min,
                _max=setting.soil_humidity_max,
                reverse=False,
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
                        action=signal,
                    )
                ),
                extra={
                    "tags": {
                        "controller": CONTROLLED_DEVICE,
                        "sprinkler-tag": tag.tag,
                        "message": loki_tag.SENSOR_NOT_UPDATED,
                    }
                },
            )

        else:
            SprinklerValve(tag=tag, power=0).save()
            controller_logger.error(
                (
                    f"[ERROR] [{CONTROLLED_DEVICE}] "
                    f"[tag={tag.tag}] "
                    f"Soil humidity SENSORS NO UPDATED "
                    f" => POWER = OFF"
                ),
                extra={
                    "tags": {
                        "controller": CONTROLLED_DEVICE,
                        "sprinkler-tag": tag.tag,
                        "message": loki_tag.SENSOR_NOT_UPDATED,
                    }
                },
            )


if __name__ == "__main__":

    while True:
        if PlantSettings.get_settings().activate_sprinklers_controller:
            main()
            time.sleep(CONTROLLERS_LOOP_EVERY)
        else:
            print("[INFO] SPRINKLERS DEACTIVATED")
            time.sleep(5)
