from rest_framework import serializers
from water.models import Config


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "water"
        model = Config
        fields = ["ph_min_level", "ph_max_level", "tds_min_level", "tds_max_level"]
