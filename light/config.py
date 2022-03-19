import django
from datetime import time
from light.models import Device, ConfigType, DailyTimeRange, Config


def set_default_config(tag: str):
    """
    Create daily config if no configuration found
    for a specific tag
    :param tag:
    :return:
    """

    config_type: str = "daily"
    config_name: str = "daily-default"
    try:
        ConfigType.objects.create(name=config_type)
    except django.db.IntegrityError:
        pass
    try:
        DailyTimeRange.objects.create(
            name=config_name,
            on_at=time(9, 00, 00),
            off_at=time(18, 00, 00),
            on_monday=True,
            on_tuesday=True,
            on_wednesday=True,
            on_thursday=True,
            on_friday=True,
            on_saturday=True,
            on_sunday=True,
        ).save()
    except django.db.IntegrityError:
        pass
    Config.objects.create(
        tag=Device.objects.get(tag=tag),
        config_type=ConfigType.objects.get(name=config_type),
        daily_config=DailyTimeRange.objects.get(name="daily-default"),
    ).save()
