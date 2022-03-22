from water.models import Device
from sprinkler.models import Controller, Config


def is_any_require_water(tag: str) -> bool:
    """
    Get controller configuration for sprinkler, filtered by
    linked water tank
    :return:
    """
    r = Controller.objects.filter(
        # filter sprinkler linked to water
        pk__in=Config.objects.filter(
            water_tag_link=Device.objects.get(tag=tag)
        ).values_list("id")
    ).values_list("water_valve_signal", flat=True)
    return True if True in r else False
