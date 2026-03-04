from rest_framework import generics, permissions
from .models import Organization
from .serializers import OrganizationSerializer


class CreateOrganizationView(generics.CreateAPIView):
    """
    Allows authenticated users to create an organization.
    The creator becomes OWNER.
    """

    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        organization = serializer.save()

        user = self.request.user
        user.organization = organization
        user.role = "OWNER"
        user.save()