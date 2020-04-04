from django.db import models


class EnclosureSensor(models.Model):
    """
    Enclose sensor reading values
    """
    created = models.DateTimeField(auto_now_add=True)
    enclosure_temperature = models.FloatField(blank=True, null=True)
    enclosure_hygrometry = models.FloatField(blank=True, null=True)
    enclosure_uv_index = models.CharField(blank=True, null=True, max_length=30)
    enclosure_co2_ppm = models.FloatField(blank=True, null=True)
    enclosure_cov_ppm = models.FloatField(blank=True, null=True)

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
