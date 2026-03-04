from rest_framework import generics
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    Public endpoint for user registration.
    """
    serializer_class = RegisterSerializer