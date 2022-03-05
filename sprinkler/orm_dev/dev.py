from sprinkler.models import *
from water.models import Device as WaterDevice

tag = "stest1"

try:
    Device.objects.get(tag=tag)
    print("True")
except Device.DoesNotExist:
    print("False")

Config.objects.get(tag=Device.objects.get(tag=tag)).updated_at

Config.objects.update_or_create(
    tag=Device.objects.get(tag=tag),
    defaults={
        "water_tag_link": WaterDevice.objects.get(tag="wtest"),
        "soil_moisture_min_level": 12,
        "soil_moisture_max_level": 20,
    },
)

Controller.objects.update_or_create(
    tag=Device.objects.get(tag=tag),
    defaults={
        "water_valve_signal": True,
    },
)


def is_any_require_water(water_tag_link: str) -> bool:
    """
    Get controller configuration for sprinkler, filtered by
    linked water tank
    :return:
    """
    r = Controller.objects.filter(
        # filter sprinkler linked to water
        pk__in=Config.objects.filter(
            water_tag_link=WaterDevice.objects.get(tag=water_tag_link)
        ).values_list("id")
    ).values_list("water_valve_signal", flat=True)
    return True if True in r else False
