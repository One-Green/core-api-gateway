from rest_framework import serializers
from sprinkler.models import ForceController


class DeviceSerializer(serializers.Serializer):
    tag = serializers.CharField(write_only=True)

    class Meta:
        ref_name = "sprinkler_device"


class ConfigSerializer(serializers.Serializer):
    soil_moisture_min_level = serializers.FloatField(write_only=True)
    soil_moisture_max_level = serializers.FloatField(write_only=True)
    water_tag_link = serializers.CharField(write_only=True, max_length=200)

    class Meta:
        ref_name = "sprinkler_config"


class ForceControllerSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "sprinkler_force_controller"
        model = ForceController
        fields = [
            "force_water_valve_signal",
            "water_valve_signal",
        ]
