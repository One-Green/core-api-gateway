from rest_framework import serializers
from light.models import ForceController


class RegistrySerializer(serializers.Serializer):
    tag = serializers.CharField(write_only=True)

    class Meta:
        ref_name = "light_registry"


class ConfigSerializer(serializers.Serializer):
    on_datetime_at = serializers.DateTimeField(write_only=True)
    off_datetime_at = serializers.DateTimeField(write_only=True)

    class Meta:
        ref_name = "light_configuration"


class ForceControllerSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "light_force_controller"
        model = ForceController
        fields = [
            "force_light_signal",
            "light_signal",
        ]
