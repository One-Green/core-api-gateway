import os
import sys
import time
from datetime import datetime
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.insert(0, os.path.abspath(".."))
django.setup()

from plant_kiper.settings import controller_logger, CONTROLLERS_LOOP_EVERY
from controllers import loki_tag
from core.utils import is_api_gateway_up
from plant_core.models import (
    PlantSettings,
    SprinklerTag,
    SprinklerController,
    WaterSensor,
    WaterController
)

while not is_api_gateway_up():
    time.sleep(30)

# give a name for controlled device
# for printing / logging purpose
CONTROLLED_DEVICE: str = "water"


def main():
    setting = PlantSettings.get_settings()
    sensor = WaterSensor.get_status()
    if sensor:
        if sensor.level < setting.water_tank_min_level:
            WaterController(level=0, power=0).save()
            controller_logger.error(
                (
                    f"[{datetime.isoformat(datetime.utcnow())}] [ERROR] [{CONTROLLED_DEVICE}] "
                    f" WATER LEVEL TOO LOW "
                    f" => POWER = OFF"
                ),
                extra={
                    "tags": {
                        "controller": CONTROLLED_DEVICE,
                        "message": loki_tag.WATER_LEVEL_TOO_LOW,
                    }
                },
            )
        else:
            for tag in SprinklerTag.objects.all():
                print(f'[{datetime.isoformat(datetime.utcnow())}] [INFO] Checking if {tag=} need water')
                if SprinklerController.objects.filter(tag=tag)[0].power:
                    WaterController(
                        level=sensor.level,
                        power=1,
                    ).save()

                    controller_logger.info(
                        (
                            f"[INFO] [{CONTROLLED_DEVICE}] "
                            f"action=0"
                        ),
                        extra={"tags": {"controller": CONTROLLED_DEVICE}},
                    )
                    break
            else:
                WaterController(
                    level=sensor.level,
                    power=0,
                ).save()

    else:
        WaterController(level=0, power=0).save()
        controller_logger.error(
            (
                f"[{datetime.isoformat(datetime.utcnow())}] [ERROR] [{CONTROLLED_DEVICE}] "
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
        if PlantSettings.get_settings().activate_water_controller:
            main()
            time.sleep(CONTROLLERS_LOOP_EVERY)
        else:
            print(f"[{datetime.isoformat(datetime.utcnow())}] [INFO] WATER DEACTIVATED .. sleep 5 sec")
            time.sleep(5)
