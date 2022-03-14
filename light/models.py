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


class Config(models.Model):
    tag = models.OneToOneField(
        Device, on_delete=models.CASCADE, related_name="light_config_tag"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    use_default_config = models.BooleanField(blank=False, null=False, default=True)
    default_config = models.OneToOneField(
        DailyTimeRange,
        on_delete=models.CASCADE,
        related_name="light_config_default_config",
    )

    use_planner_config = models.BooleanField(blank=False, null=True, default=False)
    planner_configs = models.ManyToManyField(
        CalendarRange, blank=True, related_query_name="light_config_planner_configs"
    )

    def save(self, *args, **kwargs):
        if self.use_default_config and self.use_planner_config:
            raise ValueError(
                "You can not use default config and planner config at same time, check only one"
            )
        super(Config, self).save(*args, **kwargs)

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
