# monitoring/urls.py

from django.urls import path
from .views import APILogListView

urlpatterns = [
    path("logs/", APILogListView.as_view(), name="api-logs"),
]