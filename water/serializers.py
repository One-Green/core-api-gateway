from rest_framework import serializers
from water.models import ForceController


class DeviceSerializer(serializers.Serializer):
    tag = serializers.CharField(write_only=True)

    class Meta:
        ref_name = "water_device"


class ConfigSerializer(serializers.Serializer):
    ph_min_level = serializers.FloatField(write_only=True)
    ph_max_level = serializers.FloatField(write_only=True)
    tds_min_level = serializers.FloatField(write_only=True)
    tds_max_level = serializers.FloatField(write_only=True)

    class Meta:
        ref_name = "water_config"


class ForceControllerSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "water_force_controller"
        model = ForceController
        fields = [
            "force_water_pump_signal",
            "force_nutrient_pump_signal",
            "force_ph_downer_pump_signal",
            "force_mixer_pump_signal",
            "water_pump_signal",
            "nutrient_pump_signal",
            "ph_downer_pump_signal",
            "mixer_pump_signal",
        ]
