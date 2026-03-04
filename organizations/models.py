import uuid
from django.db import models


class Organization(models.Model):
    """
    Represents a tenant in the SaaS system.
    Each organization has isolated data.
    """

    PLAN_CHOICES = (
        ("FREE", "Free"),
        ("PRO", "Pro"),
        ("ENTERPRISE", "Enterprise"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default="FREE")

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name