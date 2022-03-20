from rest_framework.viewsets import ModelViewSet
from light.serializers import (
    DeviceSerializer,
    SensorSerializer,
    ConfigSerializer,
    ConfigTypeSerializer,
    DailyTimeRangeSerializer,
    CalendarRangeSerializer,
    ControllerSerializer,
    ForceControllerSerializer,
)
from light.models import (
    Device,
    Sensor,
    Config,
    ConfigType,
    DailyTimeRange,
    CalendarRange,
    Controller,
    ForceController,
)


class DeviceView(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    search_fields = ["tag"]


class SensorView(ModelViewSet):
    """
    IoT tag based sensors live values
    only get because always updated by IoT
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    http_method_names = ["get"]
    search_fields = ["tag__tag"]


class ConfigView(ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    search_fields = ["tag__tag"]


class ConfigTypeView(ModelViewSet):
    queryset = ConfigType.objects.all()
    serializer_class = ConfigTypeSerializer
    search_fields = ["name"]


class DailyTimeRangeView(ModelViewSet):
    queryset = DailyTimeRange.objects.all()
    serializer_class = DailyTimeRangeSerializer
    search_fields = ["name"]


class CalendarRangeView(ModelViewSet):
    queryset = CalendarRange.objects.all()
    serializer_class = CalendarRangeSerializer
    search_fields = ["name"]


class ControllerView(ModelViewSet):
    """
    Iot tag based controller live action to take
    only get because always updated by Iot Controller
    """
    queryset = Controller.objects.all()
    serializer_class = ControllerSerializer
    http_method_names = ["get"]
    search_fields = ["tag__tag"]


class ForceControllerView(ModelViewSet):
    queryset = ForceController.objects.all()
    serializer_class = ForceControllerSerializer
    search_fields = ["tag__tag"]
