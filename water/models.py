from django.db import models
from datetime import datetime


class Config(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200, default="water")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ph_min_level = models.FloatField(blank=False, null=False)
    ph_max_level = models.FloatField(blank=False, null=False)
    tds_min_level = models.FloatField(blank=False, null=False)
    tds_max_level = models.FloatField(blank=False, null=False)


class Controller(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200, default="water")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    water_pump_signal = models.BooleanField(blank=False, null=False)
    nutrient_pump_signal = models.BooleanField(blank=False, null=False)
    ph_downer_pump_signal = models.BooleanField(blank=False, null=False)


class Water:

    def __init__(self):
        self.ph_min_level = 0.0
        self.ph_max_level = 0.0
        self.tds_min_level = 0.0
        self.tds_max_level = 0.0

    @staticmethod
    def get_controller_updated_datetime() -> datetime:
        return Config.objects.get(tag="water").__dict__['updated_at']

    @staticmethod
    def update_config(
            ph_min_level: float,
            ph_max_level: float,
            tds_min_level: float,
            tds_max_level: float
    ):
        Config.objects.update_or_create(
            defaults={
                "tag": "water",
                "ph_min_level": ph_min_level,
                "ph_max_level": ph_max_level,
                "tds_min_level": tds_min_level,
                "tds_max_level": tds_max_level
            }
        )
        return True

    def get_config(self):
        _ = Config.objects.get(tag="water").__dict__
        self.ph_min_level = _['ph_min_level']
        self.ph_max_level = _['ph_max_level']
        self.tds_min_level = _['tds_min_level']
        self.tds_max_level = _['tds_max_level']
        return _
