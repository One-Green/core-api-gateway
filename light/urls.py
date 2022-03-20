from rest_framework import routers
from light.views import (
    DeviceView,
    SensorView,
    ConfigView,
    ConfigTypeView,
    DailyTimeRangeView,
    CalendarRangeView,
    ControllerView,
    ForceControllerView,
)

router = routers.DefaultRouter()
router.register("device", DeviceView)
router.register("sensor", SensorView)
router.register("config", ConfigView)
router.register("config-type", ConfigTypeView)
router.register("config-daily", DailyTimeRangeView)
router.register("config-calendar", CalendarRangeView)
router.register("controller", ControllerView)
router.register("controller-force", ForceControllerView)

urlpatterns = router.urls
