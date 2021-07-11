from django.db import models
from datetime import datetime, time
from glbl.models import GlobalConfig
import pytz


class Registry(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200)


class Config(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    on_datetime_at = models.DateTimeField(blank=False, null=False)
    off_datetime_at = models.DateTimeField(blank=False, null=False)


class Controller(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    light_signal = models.BooleanField(blank=False, null=False)


class ForceController(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200)
    force_light_signal = models.BooleanField(blank=False, null=False)
    light_signal = models.BooleanField(blank=False, null=False)


class Light:
    def __init__(self):
        self.on_datetime_at: datetime
        self.off_datetime_at: datetime

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
        on_datetime_at: datetime,
        off_datetime_at: datetime,
    ):
        Config.objects.update_or_create(
            tag=tag,
            defaults={
                "on_datetime_at": on_datetime_at,
                "off_datetime_at": off_datetime_at,
            },
        )
        return True

    def get_config(self, tag: str):
        timezone = GlobalConfig().get_config()["timezone"]
        _ = Config.objects.get(tag=tag).__dict__
        self.on_datetime_at = _["on_datetime_at"].astimezone(pytz.timezone(timezone))
        self.off_datetime_at = _["off_datetime_at"].astimezone(pytz.timezone(timezone))
        return _

    @staticmethod
    def update_controller(tag: str, light_signal: bool):
        Controller.objects.update_or_create(
            tag=tag,
            defaults={
                "light_signal": light_signal,
            },
        )

    @staticmethod
    def update_controller_force(
        tag: str,
        force_light_signal: bool,
        light_signal: bool,
    ):
        ForceController.objects.update_or_create(
            tag=tag,
            defaults={
                "force_light_signal": force_light_signal,
                "light_signal": light_signal,
            },
        )
        return True

    @staticmethod
    def get_controller_force(tag):
        try:
            _ = ForceController.objects.get(tag=tag).__dict__
        except ForceController.DoesNotExist:
            _ = {"tag": tag, "force_light_signal": False, "light_signal": False}
        return _
