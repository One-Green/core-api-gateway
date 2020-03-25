from django.db import models
from django.core.exceptions import ObjectDoesNotExist


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

    activate_cooler_controller = models.BooleanField(default=True, blank=False, null=False)
    activate_heater_controller = models.BooleanField(default=True, blank=False, null=False)
    activate_air_humidifier_controller = models.BooleanField(default=True, blank=False, null=False)
    activate_uv_light_controller = models.BooleanField(default=True, blank=False, null=False)
    activate_soil_humidifier_controller = models.BooleanField(default=True, blank=False, null=False)

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
        return cls.objects.all().values()[0]


class Enclosure(models.Model):
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
        if Enclosure.objects.count() == 1000:
            Enclosure.objects.all().order_by('created')[0].delete()
        super(Enclosure, self).save(*args, **kwargs)

    @classmethod
    def get_status(cls):
        """
        get latest values
        :return:
        """
        try:
            return cls.objects.values().latest('created')
        except ObjectDoesNotExist:
            return {}

    class Meta:
        ordering = ['created']


class Cooler(models.Model):
    """
    Cooling system for temperature controller
    """
    created = models.DateTimeField(auto_now_add=True)

    air_in_temperature = models.FloatField(blank=True, null=True)
    air_in_humidity = models.FloatField(blank=True, null=True)

    air_out_temperature = models.FloatField(blank=True, null=True)
    air_out_humidity = models.FloatField(blank=True, null=True)

    cold_surface_temperature = models.FloatField(blank=True, null=True)
    hot_surface_temperature = models.FloatField(blank=True, null=True)

    power_status = models.SmallIntegerField(blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:
        """
        if Cooler.objects.all().count() == 1000:
            Cooler.objects.all().order_by('created')[0].delete()
        super(Cooler, self).save(*args, **kwargs)

    @classmethod
    def get_status(cls):
        """
        get latest values
        :return:
        """
        try:
            return cls.objects.values().latest('created')
        except ObjectDoesNotExist:
            return {}

    @classmethod
    def set_power_status(cls, new_status: int):
        """
        method shift last sensors values
        with new power status
        :param new_status:
        :return:
        """
        current_values = cls.get_status()
        cls(cold_surface_temperature=current_values.get('cold_surface_temperature'),
            hot_surface_temperature=current_values.get('hot_surface_temperature'),
            power_status=new_status).save()

    @classmethod
    def set_sensors(cls, new_sensors_values: dict):
        """
        method to shift power status with new values
        :param new_sensors_values:
        :return:
        """
        current_values = cls.get_status()
        cls(cold_surface_temperature=new_sensors_values.get('cold_surface_temperature'),
            hot_surface_temperature=new_sensors_values.get('hot_surface_temperature'),
            power_status=current_values['power_status']).save()

    class Meta:
        ordering = ['created']


class AirHumidifier(models.Model):
    """
    Air humidifier I/O
    """
    created = models.DateTimeField(auto_now_add=True)
    water_level = models.FloatField(blank=True, null=True)
    power_status = models.SmallIntegerField(blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:<
        """
        if AirHumidifier.objects.all().count() == 1000:
            AirHumidifier.objects.all().order_by('created')[0].delete()
        super(AirHumidifier, self).save(*args, **kwargs)

    @classmethod
    def get_status(cls):
        """
        get latest values
        :return:
        """
        try:
            return cls.objects.values().latest('created')
        except ObjectDoesNotExist:
            return {}

    @classmethod
    def set_power_status(cls, new_status: int):
        """
        method shift last sensors values
        with new power status
        :param new_status:
        :return:
        """
        current_values = cls.get_status()
        cls(water_level=current_values.get('water_level'),
            power_status=new_status).save()

    @classmethod
    def set_sensors(cls, new_sensors_values: dict):
        """
        method shift last sensors values
        with new power status
        :param new_sensors_values:
        :return:
        """
        current_values = cls.get_status()
        cls(water_level=new_sensors_values.get('water_level'),
            power_status=current_values['power_status']).save()

    class Meta:
        ordering = ['created']


class WaterPump(models.Model):
    """
    Water + plant nutriment tank I/O
    """
    created = models.DateTimeField(auto_now_add=True)
    water_level = models.FloatField(blank=True, null=True)
    power_status = models.SmallIntegerField(blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:
        """
        if WaterPump.objects.all().count() == 1000:
            WaterPump.objects.all().order_by('created')[0].delete()
        super(WaterPump, self).save(*args, **kwargs)

    @classmethod
    def get_status(cls):
        """
        get latest values
        :return:
        """
        try:
            return cls.objects.values().latest('created')
        except ObjectDoesNotExist:
            return {}

    @classmethod
    def set_power_status(cls, new_status: int):
        """
        method shift last sensors values
        with new power status
        :param new_status:
        :return:
        """
        current_values = cls.get_status()
        cls(water_level=current_values.get('water_level'),
            power_status=new_status).save()

    @classmethod
    def set_sensors(cls, new_sensors_values: dict):
        """
        method shift last sensors values
        with new power status
        :param new_sensors_values:
        :return:
        """
        current_values = cls.get_status()
        cls(water_level=new_sensors_values.get('water_level'),
            power_status=current_values['power_status']).save()

    class Meta:
        ordering = ['created']


class SprinklerTag(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=30, blank=False, null=False, primary_key=True)

    def __str__(self):
        return self.tag

    class Meta:
        ordering = ['created']


class SprinklerValve(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey(SprinklerTag, on_delete=models.CASCADE)
    soil_hygrometry = models.FloatField(blank=True, null=True)
    power_status = models.SmallIntegerField(blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:
        """
        if SprinklerValve.objects.all().count() == 10000:
            SprinklerValve.objects.all().order_by('created')[0].delete()
        super(SprinklerValve, self).save(*args, **kwargs)

    @classmethod
    def get_status(cls, _tag):
        """
        get latest values
        :return:
        """
        try:
            return cls.objects.get(
                tag=SprinklerTag.objects.get(
                    tag=_tag
                )
            ).latest('created')

        except ObjectDoesNotExist:
            return {}


class Heater(models.Model):
    """
    Electrical heater I/O (control enclosure temperature)
    """
    created = models.DateTimeField(auto_now_add=True)
    hot_surface_temperature = models.FloatField(blank=True, null=True)
    air_in_temperature = models.FloatField(blank=True, null=True)
    air_out_temperature = models.FloatField(blank=True, null=True)
    power_status = models.SmallIntegerField(blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:
        """
        if Heater.objects.all().count() == 1000:
            Heater.objects.all().order_by('created')[0].delete()
        super(Heater, self).save(*args, **kwargs)

    @classmethod
    def get_status(cls):
        """
        get latest values
        :return:
        """
        try:
            return cls.objects.values().latest('created')
        except ObjectDoesNotExist:
            return {}

    @classmethod
    def set_power_status(cls, new_status: int):
        """
        method shift last sensors values
        with new power status
        :param new_status:
        :return:
        """
        current_values = cls.get_status()
        cls(hot_surface_temperature=current_values.get('hot_surface_temperature'),
            air_in_temperature=current_values.get('air_in_temperature'),
            air_out_temperature=current_values.get('air_out_temperature'),
            power_status=new_status).save()

    @classmethod
    def set_sensors(cls, new_sensors_values: dict):
        """
        method shift last sensors values
        with new power status
        :param new_sensors_values:
        :return:
        """
        current_values = cls.get_status()
        cls(hot_surface_temperature=new_sensors_values.get('hot_surface_temperature'),
            air_in_temperature=new_sensors_values.get('air_in_temperature'),
            air_out_temperature=new_sensors_values.get('air_out_temperature'),
            power_status=current_values['power_status']).save()

    class Meta:
        ordering = ['created']


class UvLight(models.Model):
    """
    UV light I/O enclosure
    """
    created = models.DateTimeField(auto_now_add=True)
    power_status = models.SmallIntegerField(blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:
        """
        if UvLight.objects.all().count() == 1000:
            UvLight.objects.all().order_by('created')[0].delete()
        super(UvLight, self).save(*args, **kwargs)

    @classmethod
    def get_status(cls):
        """
        get latest values
        :return:
        """
        try:
            return cls.objects.values().latest('created')
        except ObjectDoesNotExist:
            return {}

    @classmethod
    def set_power_status(cls, new_status: int):
        """
        method shift last sensors values
        with new power status
        :param new_status:
        :return:
        """
        # lighting is based on time controller
        cls(power_status=new_status).save()

    class Meta:
        ordering = ['created']


class CO2Valve(models.Model):
    """
    CO2 ppm enclosure injection I/O
    """
    created = models.DateTimeField(auto_now_add=True)
    high_pressure = models.FloatField(blank=True, null=True)
    low_pressure = models.FloatField(blank=True, null=True)
    power_status = models.SmallIntegerField(blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:
        """
        if CO2Valve.objects.all().count() == 1000:
            CO2Valve.objects.all().order_by('created')[0].delete()
        super(CO2Valve, self).save(*args, **kwargs)

    @classmethod
    def get_status(cls):
        """
        get latest values
        :return:
        """
        try:
            return cls.objects.values().latest('created')
        except ObjectDoesNotExist:
            return {}

    @classmethod
    def set_power_status(cls, new_status: int):
        """
        method shift last sensors values
        with new power status
        :param new_status:
        :return:
        """
        current_values = cls.get_status()
        cls(high_pressure=current_values.get('high_pressure'),
            low_pressure=current_values.get('low_pressure'),
            power_status=new_status).save()

    @classmethod
    def set_sensors(cls, new_sensors_values: dict):
        """
        method shift last sensors values
        with new power status
        :param new_sensors_values:
        :return:
        """
        current_values = cls.get_status()
        cls(high_pressure=new_sensors_values.get('high_pressure'),
            low_pressure=new_sensors_values.get('low_pressure'),
            power_status=current_values['power_status']).save()

    class Meta:
        ordering = ['created']


class Filters(models.Model):
    """
    Filter delta pressure, elevated pressure mean filter's dirty
    """

    created = models.DateTimeField(auto_now_add=True)
    in_air_delta_pressure = models.FloatField(blank=True, null=True)
    out_air_delta_pressure = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        keep only 1000 latest values
        :param args:
        :param kwargs:
        :return:
        """
        if Filters.objects.all().count() == 1000:
            Filters.objects.all().order_by('created')[0].delete()
        super(Filters, self).save(*args, **kwargs)

    @classmethod
    def get_status(cls):
        """
        get latest values
        :return:
        """
        try:
            return cls.objects.values().latest('created')
        except ObjectDoesNotExist:
            return {}

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
