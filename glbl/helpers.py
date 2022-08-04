from django.core.exceptions import ValidationError
import pytz


def timezone_validator(value):
    if value not in pytz.all_timezones:
        raise ValidationError(
            f"[Error] Timezone={value} not recognized in pytz.all_timezones"
        )
