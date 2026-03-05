# monitoring/views.py

from django.db.models import Avg, Count
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from monitoring.models import APILog
from monitoring.serializers import APILogSerializer, APIMetricsSerializer
from apis.models import MonitoredAPI


class APILogListView(generics.ListAPIView):
    """
    Returns monitoring logs for the current organization.
    """

    serializer_class = APILogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        org = self.request.organization

        return APILog.objects.filter(
            monitored_api__organization=org
        ).select_related("monitored_api")


class APIMetricsView(APIView):
    """
    Returns aggregated metrics for an API.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, api_id):

        org = request.organization

        try:
            api = MonitoredAPI.objects.get(
                id=api_id,
                organization=org
            )
        except MonitoredAPI.DoesNotExist:
            return Response({"error": "API not found"}, status=404)

        logs = APILog.objects.filter(monitored_api=api)

        total_checks = logs.count()

        success_count = logs.filter(is_success=True).count()

        avg_latency = logs.aggregate(
            Avg("response_time_ms")
        )["response_time_ms__avg"] or 0

        success_rate = 0

        if total_checks > 0:
            success_rate = (success_count / total_checks) * 100

        data = {
            "total_checks": total_checks,
            "success_rate": success_rate,
            "avg_response_time": avg_latency,
        }

        serializer = APIMetricsSerializer(data)

        return Response(serializer.data)