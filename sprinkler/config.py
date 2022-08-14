import django
from project.settings import DEFAULT_WATER_DEVICE
from sprinkler.models import Device, Config, ForceController
from water.models import Device as WaterDevice


def set_default_config(tag):
    try:
        Config.objects.create(
            tag=Device.objects.get(tag=tag),
            soil_moisture_min_level=30,
            soil_moisture_max_level=70,
            water_tag_link=WaterDevice.objects.get(tag=DEFAULT_WATER_DEVICE),
        ).save()
    except django.db.IntegrityError:
        pass


def set_default_force_controller(tag):
    try:
        ForceController.objects.create(
            tag=Device.objects.get(tag=tag),
            force_water_valve_signal=False,
            water_valve_signal=False
        ).save()
    except django.db.IntegrityError:
        pass
