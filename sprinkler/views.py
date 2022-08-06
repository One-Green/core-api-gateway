from rest_framework.viewsets import ModelViewSet
from sprinkler.serializers import (
    DeviceSerializer,
    SensorSerializer,
    ConfigSerializer,
    ControllerSerializer,
    ForceControllerSerializer,
)
from sprinkler.models import Device, Sensor, Config, Controller, ForceController


class DeviceView(ModelViewSet):
    queryset = Device.objects.all().order_by('id')
    serializer_class = DeviceSerializer
    search_fields = ["tag"]


class SensorView(ModelViewSet):
    """
    IoT tag based sensors live values
    only get because always updated by IoT
    """

    queryset = Sensor.objects.all().order_by('id')
    serializer_class = SensorSerializer
    http_method_names = ["get"]
    search_fields = ["tag__tag"]


class ConfigView(ModelViewSet):
    queryset = Config.objects.all().order_by('id')
    serializer_class = ConfigSerializer
    search_fields = ["tag__tag"]


class ControllerView(ModelViewSet):
    """
    Iot tag based controller live action to take
    only get because always updated by Iot Controller
    """

    queryset = Controller.objects.all().order_by('id')
    serializer_class = ControllerSerializer
    http_method_names = ["get"]
    search_fields = ["tag__tag"]


class ForceControllerView(ModelViewSet):
    queryset = ForceController.objects.all().order_by('id')
    serializer_class = ForceControllerSerializer
    search_fields = ["tag__tag"]
