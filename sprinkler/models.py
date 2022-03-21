from django.db import models
from water.models import Device as WaterDevice


class Device(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200)

    def __str__(self):
        return f"{self.tag}"


class Sensor(models.Model):
    tag = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name="sprinkler_sensor_tag"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    soil_moisture_raw_adc = models.IntegerField(blank=False, null=False)
    soil_moisture = models.FloatField(blank=False, null=False)

    def __str__(self):
        return f"{self.tag}"


class Config(models.Model):
    tag = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name="sprinkler_config_tag"
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
        Device, on_delete=models.CASCADE, related_name="sprinkler_controller_tag"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    water_valve_signal = models.BooleanField(blank=False, null=False)

    def __str__(self):
        return f"{self.tag}"


class ForceController(models.Model):
    tag = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name="sprinkler_forceController_tag"
    )
    updated_at = models.DateTimeField(auto_now=True)
    force_water_valve_signal = models.BooleanField(blank=False, null=False)
    water_valve_signal = models.BooleanField(blank=False, null=False)

    def __str__(self):
        return f"{self.tag}"
