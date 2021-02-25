from django.db import models
from datetime import datetime


class Registry(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200)


class Config(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    soil_moisture_min_level = models.FloatField(blank=False, null=False)
    soil_moisture_max_level = models.FloatField(blank=False, null=False)


class Controller(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    water_valve_signal = models.BooleanField(blank=False, null=False)


class Sprinklers:
    def __init__(self):
        self.soil_moisture_min_level: float = 0.0
        self.soil_moisture_max_level: float = 0.0

    @staticmethod
    def get_controller_updated_datetime(tag: str) -> datetime:
        return Config.objects.get(tag=tag).__dict__["updated_at"]

    @staticmethod
    def is_tag_in_registry(tag: str) -> bool:
        if len(Registry.objects.filter(tag=tag)):
            return True
        else:
            return False

    @staticmethod
    def add_tag_in_registry(tag) -> bool:
        v, c = Registry.objects.update_or_create(tag=tag)
        return c

    @staticmethod
    def update_config(
        tag: str,
        soil_moisture_min_level: float,
        soil_moisture_max_level: float,
    ):
        Config.objects.update_or_create(
            tag=tag,
            defaults={
                "soil_moisture_min_level": soil_moisture_min_level,
                "soil_moisture_max_level": soil_moisture_max_level,
            },
        )
        return True

    def get_config(self, tag: str):
        _ = Config.objects.get(tag=tag).__dict__
        self.soil_moisture_min_level = _["soil_moisture_min_level"]
        self.soil_moisture_max_level = _["soil_moisture_max_level"]
        return _

    @staticmethod
    def update_controller(tag: str, water_valve_signal: bool):
        Controller.objects.update_or_create(
            tag=tag,
            defaults={
                "water_valve_signal": water_valve_signal,
            },
        )

    @staticmethod
    def is_any_require_water() -> bool:
        """
        Check if any of sprinkler required water
        :return:
        """
        for _ in Controller.objects.all():
            if _.water_valve_signal:
                return True

        return False
