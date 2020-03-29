from rest_framework import serializers
from plant_core.models import (
    Enclosure,
    Cooler,
    AirHumidifier,
    WaterPump,
    Heater,
    UvLight,
    CO2Valve,
    Filters,
    SimpleFlaps
)


class EnclosureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enclosure
        fields = '__all__'


class CoolerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooler
        fields = '__all__'


class AirHumidifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirHumidifier
        fields = '__all__'


class WaterPumpSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterPump
        fields = '__all__'


class SprinklerValveSerializer(serializers.Serializer):
    tag = serializers.CharField()
    # TODO fix read/write mandatory field
    # soil_hygrometry = serializers.FloatField(write_only=True)
    # power_status = serializers.IntegerField(read_only=True)


class HeaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heater
        fields = '__all__'


class UvLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = UvLight
        fields = '__all__'


class CO2ValveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CO2Valve
        fields = '__all__'


class FiltersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filters
        fields = '__all__'


class SimpleFlapsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleFlaps
        fields = '__all__'
