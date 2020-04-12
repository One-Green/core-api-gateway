from django.db import models


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
            EnclosureSensor.objects.all().order_by('created')[0].delete()
        super(EnclosureSensor, self).save(*args, **kwargs)

    @classmethod
    def __status(cls):
        """
        get latest values
        :return:
        """
        try:
            return cls.objects.values().latest('created')
        except cls.ObjectDoesNotExist:
            return None

    @property
    def status(self):
        return self.__status()

    class Meta:
        ordering = ['-created']
