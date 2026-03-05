from rest_framework import serializers
from .models import MonitoredAPI
from organizations.services import get_api_limit_for_org


class MonitoredAPISerializer(serializers.ModelSerializer):
    """
    Handles validation and plan-based enforcement.
    """

    class Meta:
        model = MonitoredAPI
        fields = "__all__"
        read_only_fields = ("id", "organization", "created_at")

    def validate_check_interval_seconds(self, value):
        """
        Prevent too aggressive monitoring on free plan.
        """
        request = self.context["request"]
        org = request.organization

        if org.plan == "FREE" and value < 300:
            raise serializers.ValidationError(
                "Free plan minimum interval is 300 seconds."
            )

        return value

    def validate(self, attrs):
        """
        Enforce plan-based API count limits.
        """
        request = self.context["request"]
        org = request.organization

        if self.instance is None:  # Only on create
            current_count = MonitoredAPI.objects.filter(
                organization=org
            ).count()

            max_allowed = get_api_limit_for_org(org)

            if current_count >= max_allowed:
                raise serializers.ValidationError(
                    "API limit reached for your subscription plan."
                )

        return attrs