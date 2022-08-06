from rest_framework import serializers
from glbl.models import Config


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "global_config"
        model = Config
        fields = "__all__"
        ordering = ['-id']
