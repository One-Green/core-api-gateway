from rest_framework import serializers


class ConfigSerializer(serializers.Serializer):
    timezone = serializers.CharField(write_only=True)

    class Meta:
        ref_name = "global_config"
