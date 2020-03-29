import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(os.path.dirname(os.path.dirname(os.path.join('..', '..', os.path.dirname('__file__')))))
django.setup()

from plant_kiper.settings import controller_logger
from plant_core.models import (
    SprinklerTag,
    SprinklerValve,
    WaterPump
)

# give a name for controlled device
# for printing / logging purpose
CONTROLLED_DEVICE: str = 'water-pump'

# Print template
# generic template for logging/print (for log remove datetime_now)
PRINT_TEMPLATE = (
    '[INFO] [{device}] ;'
    ' pump status = {action}'
)


def main():
    sprinklers_request = []
    for tag in SprinklerTag.objects.all():
        sprinklers_request.append(
            SprinklerValve.get_status(tag).power_status
        )

    if 1 in sprinklers_request:
        WaterPump.set_power_status(1)
        controller_logger.info(
            PRINT_TEMPLATE.format(
                device=CONTROLLED_DEVICE,
                action=1
            ),
            extra={"tags": {"controller": CONTROLLED_DEVICE}}
        )
    else:
        WaterPump.set_power_status(0)
        controller_logger.info(
            PRINT_TEMPLATE.format(
                device=CONTROLLED_DEVICE,
                action=0
            ),
            extra={"tags": {"controller": CONTROLLED_DEVICE}}
        )


if __name__ == '__main__':
    print(
        f'[WARNING] [{CONTROLLED_DEVICE}] device debug mode, '
        f'use controller/run.py to load controller'
    )
    while True:
        main()
