from rest_framework import serializers
from plant_core.models import (Enclosure,
                               PeltierCell,
                               VaporGenerator,
                               WaterTank,
                               ElectricalHeater,
                               UvLight,
                               CO2Valve,
                               Filters)


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


class ElectricalHeaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricalHeater
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
