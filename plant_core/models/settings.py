from django.db import models


class PlantSettings(models.Model):
    """
    Plant control parameter
    controller will try to keep these values
    """
    plant_identifier = models.CharField(blank=True, null=True, max_length=300)

    plant_type = models.CharField(blank=True, null=True, max_length=300)

    air_temperature_min = models.FloatField(blank=True, null=True)
    air_temperature_max = models.FloatField(blank=True, null=True)

    air_hygrometry_min = models.FloatField(blank=True, null=True)
    air_hygrometry_max = models.FloatField(blank=True, null=True)

    air_co2_ppm_min = models.FloatField(blank=True, null=True)
    air_co2_ppm_max = models.FloatField(blank=True, null=True)

    light_start = models.TimeField(blank=True, null=True)
    light_end = models.TimeField(blank=True, null=True)

    sprinkler_setting = models.ManyToManyField('SprinklerSettings')

    activate_cooler_controller = models.BooleanField(default=True, blank=False, null=False)
    activate_heater_controller = models.BooleanField(default=True, blank=False, null=False)
    activate_air_humidifier_controller = models.BooleanField(default=True, blank=False, null=False)
    activate_uv_light_controller = models.BooleanField(default=True, blank=False, null=False)
    activate_sprinklers_controller = models.BooleanField(default=True, blank=False, null=False)

    @property
    def lighting_duration(self):
        return self.light_end - self.light_start

    def __str__(self):
        return "Plant Settings"

    def save(self, *args, **kwargs):
        """
        keep only one plant setting in database
        :param args:
        :param kwargs:
        :return:
        """
        # if there no last config
        if not PlantSettings.objects.all().count():
            super(PlantSettings, self).save(*args, **kwargs)
        else:
            # remove last config and save new one
            PlantSettings.objects.all().delete()
            super(PlantSettings, self).save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        return cls.objects.all()[0]
