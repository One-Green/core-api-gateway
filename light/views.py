from rest_framework.viewsets import ModelViewSet
from light.serializers import (
    DeviceSerializer,
    ConfigSerializer,
    DailyTimeRangeSerializer,
    CalendarRangeSerializer,
    ControllerSerializer,
    ForceControllerSerializer,
)
from light.models import (
    Device,
    Config,
    DailyTimeRange,
    CalendarRange,
    Controller,
    ForceController,
)


class DeviceView(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    search_fields = ["tag"]


class ConfigView(ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    search_fields = ["tag"]


class DailyTimeRangeView(ModelViewSet):
    queryset = DailyTimeRange.objects.all()
    serializer_class = DailyTimeRangeSerializer
    search_fields = ["name"]


class CalendarRangeView(ModelViewSet):
    queryset = CalendarRange.objects.all()
    serializer_class = CalendarRangeSerializer
    search_fields = ["name"]


class ControllerView(ModelViewSet):
    queryset = Controller.objects.all()
    serializer_class = ControllerSerializer
    search_fields = ["tag"]


class ForceControllerView(ModelViewSet):
    queryset = ForceController.objects.all()
    serializer_class = ForceControllerSerializer
    search_fields = ["tag"]
