from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta
from pytz import utc


class WaterPumpSensor(models.Model):
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

        if WaterPumpSensor.objects.all().count() >= 30000:
            WaterPumpSensor.objects.all().order_by("created")[0].delete()
        super(WaterPumpSensor, self).save(*args, **kwargs)

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


class WaterPumpController(models.Model):
    """

    """

    created = models.DateTimeField(auto_now_add=True, primary_key=True)
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
        if WaterPumpController.objects.all().count() == 30000:
            WaterPumpController.objects.all().order_by("created")[0].delete()
        super(WaterPumpController, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created"]


class SprinklerTag(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=30, blank=False, null=False, primary_key=True)

    def __str__(self):
        return f"{self.tag}-tag"


class SprinklerSettings(models.Model):
    tag = models.OneToOneField(SprinklerTag, on_delete=models.CASCADE)
    soil_humidity_min = models.FloatField(blank=False, null=False)
    soil_humidity_max = models.FloatField(blank=False, null=False)

    def __str__(self):
        return f"{self.tag}-setting"


class SprinklerSensor(models.Model):
    created = models.DateTimeField(auto_now_add=True, primary_key=True)
    tag = models.ForeignKey(SprinklerTag, on_delete=models.CASCADE)
    soil_humidity = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.tag}-sensor"

    @classmethod
    def status(cls, tag):
        """
        get latest values
        :return:
        """

        assert isinstance(tag, SprinklerTag)
        try:
            return cls.objects.filter(
                tag=tag,
                created__gte=utc.localize(datetime.now() - timedelta(seconds=5)),
            )[0]
        except IndexError:
            return None
        except cls.ObjectDoesNotExist:
            return None

    class Meta:
        ordering = ["-created"]


class SprinklerController(models.Model):
    created = models.DateTimeField(auto_now_add=True, primary_key=True)
    tag = models.ForeignKey(SprinklerTag, on_delete=models.CASCADE)
    humidity_level = models.FloatField(null=True, blank=True)
    humidity_level_max = models.FloatField(null=True, blank=True)
    humidity_level_min = models.FloatField(null=True, blank=True)
    power = models.SmallIntegerField(
        null=False, blank=False, validators=[MaxValueValidator(1), MinValueValidator(0)]
    )

    def __str__(self):
        return f"{self.tag}-valve"

    class Meta:
        ordering = ["-created"]
