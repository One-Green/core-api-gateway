from django.db import models


class Device(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200)

    def __str__(self):
        return f"{self.tag}"


class DailyTimeRange(models.Model):
    name = models.CharField(unique=True, null=False, blank=False, max_length=200)

    on_at = models.TimeField(blank=False, null=False)
    off_at = models.TimeField(blank=False, null=False)

    on_monday = models.BooleanField(blank=False, null=False)
    on_tuesday = models.BooleanField(blank=False, null=False)
    on_wednesday = models.BooleanField(blank=False, null=False)
    on_thursday = models.BooleanField(blank=False, null=False)
    on_friday = models.BooleanField(blank=False, null=False)
    on_saturday = models.BooleanField(blank=False, null=False)
    on_sunday = models.BooleanField(blank=False, null=False)

    def save(self, *args, **kwargs):
        # check time coherence before commit
        if self.off_at <= self.on_at:
            raise ValueError(
                f"{self.off_at=} <= {self.on_at=}. "
                f"ON time must be lower than OFF time"
            )
        super(DailyTimeRange, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class CalendarRange(models.Model):
    name = models.CharField(unique=True, null=False, blank=False, max_length=200)
    start_date_at = models.DateField(blank=False, null=False)
    end_date_at = models.DateField(blank=False, null=False)
    on_time_at = models.TimeField(blank=False, null=False)
    off_time_at = models.TimeField(blank=False, null=False)

    def save(self, *args, **kwargs):
        # check time coherence before commit
        if self.off_time_at < self.on_time_at:
            raise ValueError(
                f"{self.off_time_at=} < {self.on_time_at=}. "
                f"ON time must be lower than OFF time"
            )
        if self.end_date_at < self.start_date_at:
            raise ValueError(
                f"{self.end_date_at=} < {self.start_date_at=}. "
                f"START date must be lower than START date"
            )
        super(CalendarRange, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class ConfigType(models.Model):
    """
    init.py fill which kind of light off/on amplification to use :
        - daily
        - planner
    """
    name = models.CharField(unique=True, max_length=20, blank=False, null=False)

    def __str__(self):
        return f"{self.name}"


class Config(models.Model):
    tag = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name="light_config_tag"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    config_type = models.ForeignKey(ConfigType, on_delete=models.CASCADE, related_query_name="light_config_type")

    daily_config = models.ForeignKey(
        DailyTimeRange,
        related_name="light_config_default_config",
        on_delete=models.CASCADE,
    )
    planner_configs = models.ManyToManyField(
        CalendarRange, blank=True, related_query_name="light_config_planner_configs"
    )

    def __str__(self):
        return f"{self.tag}"


class Sensor(models.Model):
    tag = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name="light_sensor_tag"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    lux_lvl = models.FloatField(blank=False, null=False)
    photo_resistor_raw = models.IntegerField(blank=False, null=False)
    photo_resistor_percent = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return f"{self.tag}"


class Controller(models.Model):
    tag = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name="light_controller_tag"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    light_signal = models.BooleanField(blank=False, null=False)

    def __str__(self):
        return f"{self.tag}"


class ForceController(models.Model):
    tag = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name="light_force_controller_tag"
    )
    force_light_signal = models.BooleanField(blank=False, null=False)
    light_signal = models.BooleanField(blank=False, null=False)

    def __str__(self):
        return f"{self.tag}"
