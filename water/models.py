from django.db import models


class Controller(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    water_pump_signal = models.BooleanField(blank=False, null=False)
    nutrient_pump_signal = models.BooleanField(blank=False, null=False)
    ph_downer_pump_signal = models.BooleanField(blank=False, null=False)
