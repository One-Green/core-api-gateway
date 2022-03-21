from django.db import models


class Device(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200)

    def __str__(self):
        return f"{self.tag}"


class Sensor(models.Model):
    tag = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name="water_sensor_tag"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ph_voltage = models.FloatField(null=False, blank=False)
    tds_voltage = models.FloatField(null=False, blank=False)
    ph_level = models.FloatField(null=False, blank=False)
    tds_level = models.FloatField(null=False, blank=False)
    water_tk_lvl = models.IntegerField(null=False, blank=False)
    nutrient_tk_lvl = models.IntegerField(null=False, blank=False)
    ph_downer_tk_lvl = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.tag}"


class Config(models.Model):
    tag = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name="water_config_tag"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ph_min_level = models.FloatField(blank=False, null=False)
    ph_max_level = models.FloatField(blank=False, null=False)
    tds_min_level = models.FloatField(blank=False, null=False)
    tds_max_level = models.FloatField(blank=False, null=False)

    def __str__(self):
        return f"{self.tag}"


class Controller(models.Model):
    tag = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name="water_controller_tag"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    water_pump_signal = models.BooleanField(blank=False, null=False)
    nutrient_pump_signal = models.BooleanField(blank=False, null=False)
    ph_downer_pump_signal = models.BooleanField(blank=False, null=False)
    mixer_pump_signal = models.BooleanField(blank=False, null=False)

    def __str__(self):
        return f"{self.tag}"


class ForceController(models.Model):
    tag = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name="water_force_controller_tag"
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

    def __str__(self):
        return f"{self.tag}"
