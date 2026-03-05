# organizations/models.py

import uuid
from django.db import models
from django.conf import settings


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

    plan = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        default="FREE"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return self.name


class OrganizationMember(models.Model):
    """
    Links users with organizations (multi-tenant membership).
    """

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("member", "Member"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organization_memberships"
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="members"
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="member"
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "organization")
        ordering = ["-joined_at"]

    def __str__(self):
        return f"{self.user} - {self.organization} ({self.role})"