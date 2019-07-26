from rest_framework import serializers
from plant_core.models import (Enclosure,
                               PeltierCell,
                               VaporGenerator,
                               WaterTank,
                               Heater,
                               UvLight,
                               CO2Valve,
                               Filters,
                               SimpleFlaps)


class EnclosureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enclosure
        fields = '__all__'


class PeltierCellSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeltierCell
        fields = '__all__'


class VaporGeneratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaporGenerator
        fields = '__all__'


class WaterTankSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterTank
        fields = '__all__'


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
