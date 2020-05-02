from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta
from pytz import utc


class WaterSensor(models.Model):
    """
    bse model streaming value from sensor
    """

    created = models.DateTimeField(auto_now_add=True, primary_key=True)
    level = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:
        """

        if WaterSensor.objects.all().count() >= 30000:
            WaterSensor.objects.all().order_by("created")[0].delete()
        super(WaterSensor, self).save(*args, **kwargs)

    @classmethod
    def __status(cls):
        """
        get latest values
        :return:
        """
        try:
            return (
                cls.objects.filter(
                    created__gte=utc.localize(datetime.now() - timedelta(seconds=5))
                )
                .order_by("-created")
                .values()[0]
            )
        except IndexError:
            return None
        except cls.ObjectDoesNotExist:
            return None

    @property
    def status(self):
        return self.__status()

    class Meta:
        ordering = ["-created"]


class WaterController(models.Model):
    """

    """

    created = models.DateTimeField(auto_now_add=True, primary_key=True)
    level = models.FloatField(null=True, blank=True)
    power = models.SmallIntegerField(
        null=False, blank=False, validators=[MaxValueValidator(1), MinValueValidator(0)]
    )

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:

        :return:
        """
        if WaterController.objects.all().count() == 30000:
            WaterController.objects.all().order_by("created")[0].delete()
        super(WaterController, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created"]
