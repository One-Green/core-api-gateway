from rest_framework import serializers


class RegistrySerializer(serializers.Serializer):
    tag = serializers.CharField()


class ConfigSerializer(serializers.Serializer):
    soil_moisture_min_level = serializers.FloatField(write_only=True)
    soil_moisture_max_level = serializers.FloatField(write_only=True)
