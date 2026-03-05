# apis/urls.py

from rest_framework.routers import DefaultRouter
from .views import MonitoredAPIViewSet

router = DefaultRouter()
router.register("", MonitoredAPIViewSet, basename="apis")

urlpatterns = router.urls