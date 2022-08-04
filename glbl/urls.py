from rest_framework import routers
from glbl.views import ConfigView

router = routers.DefaultRouter()
router.register("config", ConfigView)

urlpatterns = router.urls
