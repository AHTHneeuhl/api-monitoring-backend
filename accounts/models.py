from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    """
    Custom user model for future flexibility.
    Using UUID as primary key for better security & SaaS scaling.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    ROLE_CHOICES = (
        ("OWNER", "Owner"),
        ("ADMIN", "Admin"),
        ("MEMBER", "Member"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="MEMBER")

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email