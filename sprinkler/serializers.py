from rest_framework import serializers
from sprinkler.models import (
    Device,
    Sensor,
    Config,
    Controller,
    ForceController,
)


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "sprinkler_device"
        model = Device
        fields = "__all__"


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "sprinkler_sensor"
        model = Sensor
        fields = "__all__"


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "sprinkler_configuration"
        model = Config
        fields = "__all__"


class ControllerSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "sprinkler_controller"
        model = Controller
        fields = "__all__"


class ForceControllerSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "sprinkler_force_controller"
        model = ForceController
        fields = "__all__"
