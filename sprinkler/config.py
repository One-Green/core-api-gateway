import django
from project.settings import DEFAULT_WATER_DEVICE
from sprinkler.models import Device, Config


def set_default_config(tag):
    try:
        Config.objects.create(
            tag=Device.objects.get(tag=tag),
            soil_moisture_min_level=30,
            soil_moisture_max_level=70,
            water_tag_link=DEFAULT_WATER_DEVICE,
        ).save()
    except django.db.IntegrityError:
        pass
