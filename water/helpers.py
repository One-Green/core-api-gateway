from water.models import Device
from sprinkler.models import Controller, Config


def is_any_require_water(tag: str) -> bool:
    """
    Get controller configuration for sprinkler, filtered by
    linked water tank
    :return:
    """
    # retrieve sprinklers linked to this water tag
    for _ in Config.objects.filter(water_tag_link=Device.objects.get(tag=tag)):
        if Controller.objects.get(tag=_.tag).water_valve_signal:
            return True
    else:
        return False


def count_linked_sprinkler(tag: str) -> int:
    """
    return number of sprinkler linked with water tank
    :param tag:
    :return:
    """
    return Config.objects.filter(
        water_tag_link=Device.objects.get(tag=tag)
    ).count()
