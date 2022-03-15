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
router.register("device", DeviceView)
router.register("config", ConfigView)
router.register("config-daily", DailyTimeRangeView)
router.register("config-calendar", CalendarRangeView)
router.register("controller", ControllerView)
router.register("controller-force", ForceControllerView)

urlpatterns = router.urls
