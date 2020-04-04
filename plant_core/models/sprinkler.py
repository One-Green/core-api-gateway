from django.db import models
from datetime import datetime, timedelta
from pytz import utc


class WaterTankSensor(models.Model):
    """
    bse model streaming value from sensor
    """
    created = models.DateTimeField(auto_now_add=True)
    level = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:
        """

        if WaterTankSensor.objects.all().count() >= 30000:
            WaterTankSensor.objects.all().order_by('created')[0].delete()
        super(WaterTankSensor, self).save(*args, **kwargs)

    @classmethod
    def __status(cls):
        """
        get latest values
        :return:
        """
        try:
            return cls.objects.filter(
                created__gte=utc.localize(
                    datetime.now() - timedelta(seconds=5)
                )
            ).order_by('-created').values()[0]
        except IndexError:
            return None
        except cls.ObjectDoesNotExist:
            return None

    @property
    def status(self):
        return self.__status()

    class Meta:
        ordering = ['-created']


class WaterPump(models.Model):
    """

    """
    created = models.DateTimeField(auto_now_add=True)
    power = models.BooleanField(null=False, blank=False)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:

        :return:
        """
        if WaterPump.objects.all().count() == 30000:
            WaterPump.objects.all().order_by('created')[0].delete()
        super(WaterPump, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created']


class SprinklerTag(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=30, blank=False, null=False, primary_key=True)

    def __str__(self):
        return f'{self.tag}-tag'


class SprinklerSettings(models.Model):
    tag = models.OneToOneField(SprinklerTag, on_delete=models.CASCADE)
    soil_humidity_min = models.FloatField(blank=False, null=False)
    soil_humidity_max = models.FloatField(blank=False, null=False)

    def __str__(self):
        return f'{self.tag}-setting'


class SprinklerSoilHumiditySensor(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey(SprinklerTag, on_delete=models.CASCADE)
    soil_humidity = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.tag}-sensor'

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
                created__gte=utc.localize(
                    datetime.now() - timedelta(seconds=5)
                )
            )[0]
        except IndexError:
            return None
        except cls.ObjectDoesNotExist:
            return None

    class Meta:
        ordering = ['-created']


class SprinklerValve(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey(SprinklerTag, on_delete=models.CASCADE)
    power = models.BooleanField(null=False, blank=False, default=False)
    humidity_level = models.FloatField(null=True, blank=True)
    humidity_level_max = models.FloatField(null=True, blank=True)
    humidity_level_min = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.tag}-valve'

    class Meta:
        ordering = ['-created']
