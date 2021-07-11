from rest_framework import serializers
from water.models import Config, ForceController


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "water"
        model = Config
        fields = ["ph_min_level", "ph_max_level", "tds_min_level", "tds_max_level"]


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
