import uuid
from django.db import models
from common.models import TenantAwareModel


class MonitoredAPI(TenantAwareModel):
    """
    Represents an API endpoint registered by an organization
    to be monitored periodically.
    """

    METHOD_CHOICES = (
        ("GET", "GET"),
        ("POST", "POST"),
        ("PUT", "PUT"),
        ("DELETE", "DELETE"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    base_url = models.URLField()

    method = models.CharField(
        max_length=10,
        choices=METHOD_CHOICES,
        default="GET"
    )

    headers = models.JSONField(blank=True, null=True)

    expected_status = models.IntegerField(default=200)

    check_interval_seconds = models.IntegerField(default=60)

    timeout_seconds = models.IntegerField(default=10)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["organization"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.base_url}"