# apis/serializers.py

from rest_framework import serializers
from apis.models import MonitoredAPI
from organizations.services import get_api_limit_for_org


class MonitoredAPISerializer(serializers.ModelSerializer):
    """
    Serializer for creating and managing monitored APIs.
    Enforces plan limits and validation rules.
    """

    class Meta:
        model = MonitoredAPI
        fields = "__all__"
        read_only_fields = ("id", "organization", "created_at")

    def validate_check_interval_seconds(self, value):
        """
        Prevent aggressive monitoring for FREE plan.
        """
        request = self.context["request"]
        org = request.organization

        if org.plan == "FREE" and value < 300:
            raise serializers.ValidationError(
                "Free plan minimum monitoring interval is 300 seconds."
            )

        return value

    def validate(self, attrs):
        """
        Enforce subscription plan API limits.
        """
        request = self.context["request"]
        org = request.organization

        if self.instance is None:  # Only when creating new API
            current_count = MonitoredAPI.objects.filter(
                organization=org
            ).count()

            max_allowed = get_api_limit_for_org(org)

            if current_count >= max_allowed:
                raise serializers.ValidationError(
                    "API limit reached for your subscription plan."
                )

        return attrs

    def create(self, validated_data):
        """
        Automatically attach organization from request context.
        """
        request = self.context["request"]

        validated_data["organization"] = request.organization

        return super().create(validated_data)