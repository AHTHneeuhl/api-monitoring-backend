from rest_framework.routers import DefaultRouter
from .views import MonitoredAPIViewSet

router = DefaultRouter()
router.register(r"apis", MonitoredAPIViewSet, basename="apis")

urlpatterns = router.urls