from rest_framework import serializers
from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer for creating organizations.
    """

    class Meta:
        model = Organization
        fields = ["id", "name", "plan"]
        read_only_fields = ["id", "plan"]