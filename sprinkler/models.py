from django.db import models
from datetime import datetime
from water.models import Device as WaterDevice


class Device(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200)

    def __str__(self):
        return f"{self.tag}"


class Config(models.Model):
    tag = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name="sprinkler_Config_tag"
    )
    water_tag_link = models.ForeignKey(WaterDevice, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    soil_moisture_min_level = models.FloatField(blank=False, null=False)
    soil_moisture_max_level = models.FloatField(blank=False, null=False)

    def __str__(self):
        return f"{self.tag}"


class Controller(models.Model):
    tag = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name="sprinkler_Controller_tag"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    water_valve_signal = models.BooleanField(blank=False, null=False)

    def __str__(self):
        return f"{self.tag}"


class ForceController(models.Model):
    tag = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name="sprinkler_ForceController_tag"
    )
    updated_at = models.DateTimeField(auto_now=True)
    force_water_valve_signal = models.BooleanField(blank=False, null=False)
    water_valve_signal = models.BooleanField(blank=False, null=False)

    def __str__(self):
        return f"{self.tag}"


class Sprinklers:
    def __init__(self):
        self.water_tag_link = "not_linked_to_water"
        self.soil_moisture_min_level: float = 0.0
        self.soil_moisture_max_level: float = 0.0

    @staticmethod
    def get_controller_updated_datetime(tag: str) -> datetime:
        return Config.objects.get(tag=Device.objects.get(tag=tag)).updated_at

    @staticmethod
    def is_tag_in_registry(tag: str) -> bool:
        try:
            Device.objects.get(tag=tag)
            return True
        except Device.DoesNotExist:
            return False

    @staticmethod
    def add_tag_in_registry(tag) -> bool:
        v, c = Device.objects.update_or_create(tag=tag)
        return c

    @staticmethod
    def update_config(
        tag: str,
        water_tag_link: str,
        soil_moisture_min_level: float,
        soil_moisture_max_level: float,
    ):
        Config.objects.update_or_create(
            tag=Device.objects.get(tag=tag),
            defaults={
                "water_tag_link": WaterDevice.objects.get(tag=water_tag_link),
                "soil_moisture_min_level": soil_moisture_min_level,
                "soil_moisture_max_level": soil_moisture_max_level,
            },
        )
        return True

    def get_config(self, tag: str):
        _ = Config.objects.get(tag=Device.objects.get(tag=tag)).__dict__
        _["water_tag_link"] = WaterDevice.objects.get(id=_["water_tag_link_id"]).tag
        self.water_tag_link = _["water_tag_link"]
        self.soil_moisture_min_level = _["soil_moisture_min_level"]
        self.soil_moisture_max_level = _["soil_moisture_max_level"]
        return _

    @staticmethod
    def update_controller(tag: str, water_valve_signal: bool):
        Controller.objects.update_or_create(
            tag=Device.objects.get(tag=tag),
            defaults={
                "water_valve_signal": water_valve_signal,
            },
        )

    @staticmethod
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

    @staticmethod
    def update_controller_force(
        tag: str,
        force_water_valve_signal: bool,
        water_valve_signal: bool,
    ):
        ForceController.objects.update_or_create(
            tag=Device.objects.get(tag=tag),
            defaults={
                "force_water_valve_signal": force_water_valve_signal,
                "water_valve_signal": water_valve_signal,
            },
        )
        return True

    @staticmethod
    def get_controller_force(tag):
        try:
            _ = ForceController.objects.get(tag=Device.objects.get(tag=tag)).__dict__
        except ForceController.DoesNotExist:
            _ = {
                "tag": tag,
                "force_water_valve_signal": False,
                "water_valve_signal": False,
            }
        return _
