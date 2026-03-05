from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import MonitoredAPI
from .serializers import MonitoredAPISerializer


class MonitoredAPIViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for MonitoredAPI.
    Automatically scoped to organization.
    """

    serializer_class = MonitoredAPISerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensures users only access APIs inside their organization.
        """
        return MonitoredAPI.objects.filter(
            organization=self.request.organization
        )

    def perform_create(self, serializer):
        """
        Automatically assign organization.
        """
        serializer.save(organization=self.request.organization)

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