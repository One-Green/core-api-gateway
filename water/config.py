import django
from water.models import Device, Config


def set_default_config(tag):
    try:
        Config.objects.create(
            tag=Device.objects.get(tag=tag),
            ph_min_level=7.2,
            ph_max_level=7.8,
            tds_min_level=100,
            tds_max_level=200,
        ).save()
    except django.db.IntegrityError:
        pass
