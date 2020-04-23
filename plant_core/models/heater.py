from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta
from pytz import utc


class HeaterSensor(models.Model):
    """
    write by API Gateway
    read by controller
    """

    created = models.DateTimeField(auto_now_add=True, primary_key=True)
    air_in_temperature = models.FloatField(null=True, blank=True)
    air_out_temperature = models.FloatField(null=True, blank=True)

    air_in_humidity = models.FloatField(null=True, blank=True)
    air_out_humidity = models.FloatField(null=True, blank=True)

    heater_temperature = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        keep only 30 000 latest values
        :param args:
        :param kwargs:
        :return:
        """

        if HeaterSensor.objects.all().count() >= 30000:
            HeaterSensor.objects.all().order_by("created")[0].delete()
        super(HeaterSensor, self).save(*args, **kwargs)

    @classmethod
    def get_status(cls):
        """
        get latest values
        :return:
        """
        try:
            return cls.objects.filter(
                created__gte=utc.localize(datetime.now() - timedelta(seconds=5))
            ).order_by("-created")[0]
        except IndexError:
            return None
        except cls.ObjectDoesNotExist:
            return None


class Heater(models.Model):
    """
    write by controller
    read by api gateway
    """

    created = models.DateTimeField(auto_now_add=True, primary_key=True)
    enclosure_temperature = models.FloatField(null=True, blank=True)
    temperature_in = models.FloatField(null=True, blank=True)
    temperature_level_max = models.FloatField(null=True, blank=True)
    temperature_level_min = models.FloatField(null=True, blank=True)
    power = models.SmallIntegerField(
        null=False, blank=False, validators=[MaxValueValidator(1), MinValueValidator(0)]
    )

    class Meta:
        ordering = ["-created"]
