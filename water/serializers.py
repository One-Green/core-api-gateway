from rest_framework import serializers
from water.models import (
    Device,
    Sensor,
    Config,
    Controller,
    ForceController,
)


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "water_device"
        model = Device
        fields = "__all__"


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "water_sensor"
        model = Sensor
        fields = "__all__"


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "water_configuration"
        model = Config
        fields = "__all__"


class ControllerSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "water_controller"
        model = Controller
        fields = "__all__"


class ForceControllerSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "water_force_controller"
        model = ForceController
        fields = "__all__"
