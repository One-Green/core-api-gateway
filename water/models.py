from django.db import models
from datetime import datetime


class Registry(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200)


class Config(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ph_min_level = models.FloatField(blank=False, null=False)
    ph_max_level = models.FloatField(blank=False, null=False)
    tds_min_level = models.FloatField(blank=False, null=False)
    tds_max_level = models.FloatField(blank=False, null=False)


class Controller(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    water_pump_signal = models.BooleanField(blank=False, null=False)
    nutrient_pump_signal = models.BooleanField(blank=False, null=False)
    ph_downer_pump_signal = models.BooleanField(blank=False, null=False)
    mixer_pump_signal = models.BooleanField(blank=False, null=False)


class ForceController(models.Model):
    tag = models.CharField(
        unique=True, null=False, blank=False, max_length=200
    )
    updated_at = models.DateTimeField(auto_now=True)
    force_water_pump_signal = models.BooleanField(blank=False, null=False)
    force_nutrient_pump_signal = models.BooleanField(blank=False, null=False)
    force_ph_downer_pump_signal = models.BooleanField(blank=False, null=False)
    force_mixer_pump_signal = models.BooleanField(blank=False, null=False)
    water_pump_signal = models.BooleanField(blank=False, null=False)
    nutrient_pump_signal = models.BooleanField(blank=False, null=False)
    ph_downer_pump_signal = models.BooleanField(blank=False, null=False)
    mixer_pump_signal = models.BooleanField(blank=False, null=False)


class Water:
    def __init__(self):
        self.ph_min_level = 0.0
        self.ph_max_level = 0.0
        self.tds_min_level = 0.0
        self.tds_max_level = 0.0

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
    def add_tag_in_registry(tag: str) -> bool:
        v, c = Registry.objects.update_or_create(tag=tag)
        return c

    @staticmethod
    def update_config(
            tag: str,
            ph_min_level: float,
            ph_max_level: float,
            tds_min_level: float,
            tds_max_level: float,
    ):
        Config.objects.update_or_create(
            tag=tag,
            defaults={
                "ph_min_level": ph_min_level,
                "ph_max_level": ph_max_level,
                "tds_min_level": tds_min_level,
                "tds_max_level": tds_max_level,
            }
        )
        return True

    def get_config(self, tag: str):
        try:
            _ = Config.objects.get(tag=tag).__dict__
        except IndexError:
            return {
                "ph_min_level": "not_set",
                "ph_max_level": "not_set",
                "tds_min_level": "not_set",
                "tds_max_level": "not_set",
            }
        self.ph_min_level = _["ph_min_level"]
        self.ph_max_level = _["ph_max_level"]
        self.tds_min_level = _["tds_min_level"]
        self.tds_max_level = _["tds_max_level"]
        return _

    @staticmethod
    def update_controller_force(
            tag: str,
            force_water_pump_signal: bool,
            force_nutrient_pump_signal: bool,
            force_ph_downer_pump_signal: bool,
            force_mixer_pump_signal: bool,
            water_pump_signal: bool,
            nutrient_pump_signal: bool,
            ph_downer_pump_signal: bool,
            mixer_pump_signal: bool,
    ):
        ForceController.objects.update_or_create(
            tag=tag,
            defaults={
                "force_water_pump_signal": force_water_pump_signal,
                "force_nutrient_pump_signal": force_nutrient_pump_signal,
                "force_ph_downer_pump_signal": force_ph_downer_pump_signal,
                "force_mixer_pump_signal": force_mixer_pump_signal,
                "water_pump_signal": water_pump_signal,
                "nutrient_pump_signal": nutrient_pump_signal,
                "ph_downer_pump_signal": ph_downer_pump_signal,
                "mixer_pump_signal": mixer_pump_signal,
            }
        )
        return True

    @staticmethod
    def get_controller_force(tag):
        try:
            _ = ForceController.objects.get(tag=tag).__dict__
        except IndexError:
            return {
                "force_water_pump_signal": False,
                "force_nutrient_pump_signal": False,
                "force_ph_downer_pump_signal": False,
                "force_mixer_pump_signal": False,
                "water_pump_signal": False,
                "nutrient_pump_signal": False,
                "ph_downer_pump_signal": False,
                "mixer_pump_signal": False,
            }
        return _
