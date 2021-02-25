from rest_framework import serializers


class RegistrySerializer(serializers.Serializer):
    tag = serializers.CharField(write_only=True)

    class Meta:
        ref_name = "light"


class ConfigSerializer(serializers.Serializer):
    on_datetime_at = serializers.DateTimeField(write_only=True)
    off_datetime_at = serializers.DateTimeField(write_only=True)

    class Meta:
        ref_name = "light"
