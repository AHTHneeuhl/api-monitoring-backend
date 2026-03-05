# monitoring/serializers.py

from rest_framework import serializers
from monitoring.models import APILog


class APILogSerializer(serializers.ModelSerializer):
    """
    Serializer for raw API monitoring logs.
    """

    class Meta:
        model = APILog
        fields = [
            "id",
            "monitored_api",
            "status_code",
            "response_time_ms",
            "is_success",
            "error_message",
            "checked_at",
        ]
        read_only_fields = fields


class APIMetricsSerializer(serializers.Serializer):
    """
    Serializer for aggregated monitoring metrics.
    """

    total_checks = serializers.IntegerField()
    success_rate = serializers.FloatField()
    avg_response_time = serializers.FloatField()