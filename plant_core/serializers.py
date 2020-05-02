from rest_framework import serializers
from plant_core.models import (
    EnclosureSensor,
    HeaterSensor,
    CoolerSensor,
    AirHumidifierSensor,
    WaterSensor
)


class EnclosureSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnclosureSensor
        fields = "__all__"


class SprinklerSerializer(serializers.Serializer):
    tag = serializers.CharField()
    soil_humidity = serializers.FloatField(write_only=True)
    power = serializers.BooleanField(read_only=True, default=False)


class HeaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaterSensor
        fields = "__all__"


class CoolerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoolerSensor
        fields = "__all__"


class AirHumidifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirHumidifierSensor
        fields = "__all__"


class WaterSeriralizer(serializers.ModelSerializer):
    class Meta:
        model = WaterSensor
        fields = "__all__"
