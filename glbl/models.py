from django.db import models
from django.core.exceptions import ValidationError
import pytz


def timezone_validator(value):
    if value not in pytz.all_timezones:
        raise ValidationError(f'[Error] Timezone={value} not recognized in pytz.all_timezones')


class Config(models.Model):
    timezone = models.TextField(
        unique=True,
        null=False,
        blank=False,
        validators=[timezone_validator]
    )


class GlobalConfig:

    def __init__(self):
        pass  # Global model wrapper to use update_or_create

    @staticmethod
    def update_config(
            data
    ):
        timezone_validator(data["timezone"])
        Config.objects.update_or_create(
            defaults={
                "timezone": data["timezone"],
            }
        )
        return True

    @staticmethod
    def get_config():
        r = {}
        try:
            r = Config.objects.all().values()[0]
        except Config.DoesNotExist:
            pass
        except IndexError:
            pass
        return r
