import django
from water.models import Device, Config, ForceController


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


def set_default_force_controller(tag):
    try:
        ForceController.objects.create(
            tag=Device.objects.get(tag=tag),
            force_water_pump_signal=False,
            force_nutrient_pump_signal=False,
            force_ph_downer_pump_signal=False,
            force_mixer_pump_signal=False,
            water_pump_signal=False,
            nutrient_pump_signal=False,
            ph_downer_pump_signal=False,
            mixer_pump_signal=False
        ).save()
    except django.db.IntegrityError:
        pass
