import pytz
from django.db import models
from datetime import datetime
from glbl.models import GlobalConfig


class Device(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200)

    def __str__(self):
        return f"{self.tag}"


class DailyTimeRange(models.Model):
    name = models.CharField(unique=True, null=False, blank=False, max_length=200)

    on_at = models.TimeField(blank=False, null=False)
    off_at = models.TimeField(blank=False, null=False)

    on_monday = models.BooleanField(blank=False, null=False)
    on_tuesday = models.BooleanField(blank=False, null=False)
    on_wednesday = models.BooleanField(blank=False, null=False)
    on_thursday = models.BooleanField(blank=False, null=False)
    on_friday = models.BooleanField(blank=False, null=False)
    on_saturday = models.BooleanField(blank=False, null=False)
    on_sunday = models.BooleanField(blank=False, null=False)

    def save(self, *args, **kwargs):
        # check time coherence before commit
        if self.off_at <= self.on_at:
            raise ValueError(
                f"{self.off_at=} <= {self.on_at=}. "
                f"ON time must be lower than OFF time"
                             )
        super(DailyTimeRange, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

class Config(models.Model):
    tag = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name="light_Config_tag"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    use_default_config = models.BooleanField(blank=False, null=False)
    default_config = models.OneToOneField(DailyTimeRange, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tag}"


class Controller(models.Model):
    tag = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name="light_Controller_tag"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    light_signal = models.BooleanField(blank=False, null=False)

    def __str__(self):
        return f"{self.tag}"


class ForceController(models.Model):
    tag = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name="light_ForceController_tag"
    )
    force_light_signal = models.BooleanField(blank=False, null=False)
    light_signal = models.BooleanField(blank=False, null=False)

    def __str__(self):
        return f"{self.tag}"


class Light:
    def __init__(self):
        self.on_datetime_at: datetime
        self.off_datetime_at: datetime

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
            on_datetime_at: datetime,
            off_datetime_at: datetime,
    ):
        Config.objects.update_or_create(
            tag=Device.objects.get(tag=tag),
            defaults={
                "on_datetime_at": on_datetime_at,
                "off_datetime_at": off_datetime_at,
            },
        )
        return True

    def get_config(self, tag: str):
        timezone = GlobalConfig().get_config()["timezone"]
        _ = Config.objects.get(tag=Device.objects.get(tag=tag)).__dict__
        self.on_datetime_at = _["on_datetime_at"].astimezone(pytz.timezone(timezone))
        self.off_datetime_at = _["off_datetime_at"].astimezone(pytz.timezone(timezone))
        return _

    @staticmethod
    def update_controller(tag: str, light_signal: bool):
        Controller.objects.update_or_create(
            tag=Device.objects.get(tag=tag),
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
            tag=Device.objects.get(tag=tag),
            defaults={
                "force_light_signal": force_light_signal,
                "light_signal": light_signal,
            },
        )
        return True

    @staticmethod
    def get_controller_force(tag):
        try:
            _ = ForceController.objects.get(tag=Device.objects.get(tag=tag)).__dict__
        except ForceController.DoesNotExist:
            _ = {"tag": tag, "force_light_signal": False, "light_signal": False}
        return _
