# apis/views.py

from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from apis.models import MonitoredAPI
from apis.serializers import MonitoredAPISerializer


class MonitoredAPIViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for MonitoredAPI.

    All queries are automatically scoped to the user's organization
    to enforce multi-tenant isolation.
    """

    serializer_class = MonitoredAPISerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Only return APIs belonging to the current organization.
        """
        org = self.request.organization

        return MonitoredAPI.objects.filter(
            organization=org
        ).order_by("-created_at")

    def perform_create(self, serializer):
        """
        Automatically attach the organization.
        """
        serializer.save(
            organization=self.request.organization
        )

    def perform_update(self, serializer):
        """
        Prevent cross-tenant updates.
        """
        if serializer.instance.organization != self.request.organization:
            raise PermissionDenied("Cross-tenant access denied.")

        serializer.save()

    def perform_destroy(self, instance):
        """
        Prevent cross-tenant deletes.
        """
        if instance.organization != self.request.organization:
            raise PermissionDenied("Cross-tenant access denied.")

        instance.delete()