from rest_framework import routers
from light.views import (
    DeviceView,
    ConfigView,
    DailyTimeRangeView,
    CalendarRangeView,
    ControllerView,
    ForceControllerView,
)

router = routers.DefaultRouter()
router.register("light/device", DeviceView)
router.register("light/config", ConfigView)
router.register("light/config/daily", DailyTimeRangeView)
router.register("light/config/calendar", CalendarRangeView)
router.register("light/controller", ControllerView)
router.register("light/controller/force", ForceControllerView)
