from django.db import models


class PlantSettings(models.Model):
    """
    Plant control parameter
    controller will try to keep these values
    """
    plant_identifier = models.CharField(blank=True, null=True, max_length=300)

    plant_type = models.CharField(blank=True, null=True, max_length=300)

    air_temperature = models.FloatField(blank=True, null=True)
    air_hygrometry = models.FloatField(blank=True, null=True)
    air_co2_ppm = models.FloatField(blank=True, null=True)

    soil_hygrometry = models.FloatField(blank=True, null=True)

    light_start = models.TimeField(blank=True, null=True)
    light_end = models.TimeField(blank=True, null=True)

    @property
    def lighting_duration(self):
        return self.light_end - self.light_start

    def save(self, *args, **kwargs):
        """
        keep only one plant setting in database
        :param args:
        :param kwargs:
        :return:
        """
        if not PlantSettings.objects.all().count():
            super(PlantSettings, self).save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        return cls.objects.all().values()[0]


class Enclosure(models.Model):
    """
    Enclose sensor reading values
    """
    created = models.DateTimeField(auto_now_add=True)
    enclosure_temperature = models.FloatField(blank=True, null=True)
    enclosure_hygrometry = models.FloatField(blank=True, null=True)
    enclosure_lightning = models.FloatField(blank=True, null=True)
    enclosure_air_co2_ppm = models.FloatField(blank=True, null=True)
    enclosure_cov_ppm = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:
        """
        if Enclosure.objects.count() == 1000:
            Enclosure.objects[0].delete()
        super(Enclosure, self).save(*args, **kwargs)

    @classmethod
    def get_status(cls):
        """
        get latest values
        :return:
        """
        return cls.objects.values().latest('created')

    class Meta:
        ordering = ['created']


class PeltierCell(models.Model):
    """
    Peltier cell controller (for cooling)
    """
    created = models.DateTimeField(auto_now_add=True)
    cold_surface_temperature = models.FloatField(blank=True, null=True)
    hot_surface_temperature = models.FloatField(blank=True, null=True)
    power_status = models.BooleanField(blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:
        """
        if PeltierCell.objects.count() == 1000:
            PeltierCell.objects[0].delete()
        super(PeltierCell, self).save(*args, **kwargs)

    @classmethod
    def get_status(cls):
        """
        get latest values
        :return:
        """
        return cls.objects.values().latest('created')

    class Meta:
        ordering = ['created']


class VaporGenerator(models.Model):
    """
    Vapor generator enclosure hygromety I/O
    """
    created = models.DateTimeField(auto_now_add=True)
    water_level = models.FloatField(blank=True, null=True)
    pump_power_status = models.BooleanField(blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:
        """
        if VaporGenerator.objects.count() == 1000:
            VaporGenerator.objects[0].delete()
        super(VaporGenerator, self).save(*args, **kwargs)

    @classmethod
    def get_status(cls):
        """
        get latest values
        :return:
        """
        return cls.objects.values().latest('created')

    class Meta:
        ordering = ['created']


class WaterTank(models.Model):
    """
    Water + plant nutriment tank I/O
    """
    created = models.DateTimeField(auto_now_add=True)
    water_level = models.FloatField(blank=True, null=True)
    pump_power_status = models.BooleanField(blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:
        """
        if WaterTank.objects.count() == 1000:
            WaterTank.objects[0].delete()
        super(WaterTank, self).save(*args, **kwargs)

    @classmethod
    def get_status(cls):
        """
        get latest values
        :return:
        """
        return cls.objects.values().latest('created')

    class Meta:
        ordering = ['created']


class Heater(models.Model):
    """
    Electrical heater I/O (control enclosure temperature)
    """
    created = models.DateTimeField(auto_now_add=True)
    hot_surface_temperature = models.FloatField(blank=True, null=True)
    air_in_temperature = models.FloatField(blank=True, null=True)
    air_out_temperature = models.FloatField(blank=True, null=True)
    power_status = models.BooleanField(blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:
        """
        if Heater.objects.count() == 1000:
            Heater.objects[0].delete()
        super(Heater, self).save(*args, **kwargs)

    @classmethod
    def get_status(cls):
        """
        get latest values
        :return:
        """
        return cls.objects.values().latest('created')

    class Meta:
        ordering = ['created']


class UvLight(models.Model):
    """
    UV light I/O enclosure
    """
    created = models.DateTimeField(auto_now_add=True)
    power_status = models.BooleanField(blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:
        """
        if UvLight.objects.count() == 1000:
            UvLight.objects[0].delete()
        super(UvLight, self).save(*args, **kwargs)

    @classmethod
    def get_status(cls):
        """
        get latest values
        :return:
        """
        return cls.objects.values().latest('created')

    class Meta:
        ordering = ['created']


class CO2Valve(models.Model):
    """
    CO2 ppm enclosure injection I/O
    """
    created = models.DateTimeField(auto_now_add=True)
    high_pressure = models.FloatField(blank=True, null=True)
    low_pressure = models.FloatField(blank=True, null=True)
    valve_power_status = models.BooleanField(blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:
        """
        if CO2Valve.objects.count() == 1000:
            CO2Valve.objects[0].delete()
        super(CO2Valve, self).save(*args, **kwargs)

    @classmethod
    def get_status(cls):
        """
        get latest values
        :return:
        """
        return cls.objects.values().latest('created')

    class Meta:
        ordering = ['created']


class Filters(models.Model):
    """
    Filter delta pressure, elevated pressure mean filter's dirty
    """

    created = models.DateTimeField(auto_now_add=True)
    clean_air_in_delta_pressure = models.FloatField(blank=True, null=True)
    dirty_air_out_delta_pressure = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:
        """
        if Filters.objects.count() == 1000:
            Filters.objects[0].delete()
        super(Filters, self).save(*args, **kwargs)

    @classmethod
    def get_status(cls):
        """
        get latest values
        :return:
        """
        return cls.objects.values().latest('created')

    class Meta:
        ordering = ['created']


class SimpleFlaps(models.Model):
    """
    Air flap model
    ========================
    Full new air :
    ========================
      Flap1 clean air
      open
    >-[/]---*------------------>
            |
           [/] Flap3 recycling
            |  close
    <-[/]---*------------------<
      Flap2 dirty air
      open

    ========================
    Full recycled air :
    ========================
      Flap1 clean air
      close
    >-[/]---*------------------>
            |
           [/] Flap3 recycling
            |  open
    <-[/]---*------------------<
      Flap2 dirty air
      close
    """

    created = models.DateTimeField(auto_now_add=True)
    # limit sensors
    dirty_air_limit_sensor = models.BooleanField(blank=True, null=True, default=0)
    clean_air_limit_sensor = models.BooleanField(blank=True, null=True, default=0)
    mixin_air_limit_sensor = models.BooleanField(blank=True, null=True, default=0)
    # by default = full new air configuration
    dirty_air_flap_status = models.BooleanField(blank=True, null=True, default=1)
    clean_air_flap_status = models.BooleanField(blank=True, null=True, default=1)
    mixin_air_flap_status = models.BooleanField(blank=True, null=True, default=0)
