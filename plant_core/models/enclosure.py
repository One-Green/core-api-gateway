from django.db import models
from datetime import datetime, timedelta
from pytz import utc


class EnclosureSensor(models.Model):
    """
    Enclose sensor reading values
    """

    created = models.DateTimeField(auto_now_add=True, primary_key=True)
    temperature = models.FloatField(blank=True, null=True)
    humidity = models.FloatField(blank=True, null=True)
    uv_index = models.CharField(blank=True, null=True, max_length=30)
    co2_ppm = models.FloatField(blank=True, null=True)
    cov_ppm = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:
        """
        if EnclosureSensor.objects.count() == 30000:
            EnclosureSensor.objects.all().order_by("created")[0].delete()
        super(EnclosureSensor, self).save(*args, **kwargs)

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

    class Meta:
        ordering = ["-created"]
