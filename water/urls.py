from rest_framework import routers
from water.views import (
    DeviceView,
    SensorView,
    ConfigView,
    ControllerView,
    ForceControllerView,
)

router = routers.DefaultRouter()
router.register("device", DeviceView)
router.register("sensor", SensorView)
router.register("config", ConfigView)
router.register("controller", ControllerView)
router.register("controller-force", ForceControllerView)

urlpatterns = router.urls
