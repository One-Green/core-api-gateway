from rest_framework import serializers
from plant_core.models import (
    EnclosureSensor
)


class EnclosureSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnclosureSensor
        fields = '__all__'


class SprinklerSerializer(serializers.Serializer):
    tag = serializers.CharField()
    soil_humidity = serializers.FloatField(write_only=True)
    power = serializers.BooleanField(read_only=True, default=False)

