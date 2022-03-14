from rest_framework import serializers
from light.models import (
    Device,
    Config,
    DailyTimeRange,
    CalendarRange,
    Controller,
    ForceController,
)


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "light_device"
        model = Device
        fields = "__all__"


class DailyTimeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "light_configuration_daily_time_range"
        model = DailyTimeRange
        fields = "__all__"


class CalendarRangeSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "light_configuration_calendar_range"
        model = CalendarRange
        fields = "__all__"


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "light_configuration"
        model = Config
        fields = "__all__"


class ControllerSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "light_controller"
        model = Controller
        fields = "__all__"


class ForceControllerSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "light_force_controller"
        model = ForceController
        fields = "__all__"
