# monitoring/models.py

import uuid
from django.db import models
from django.utils import timezone


class APILog(models.Model):
    """
    Stores results of each monitoring check.

    This table will grow very large in production,
    therefore indexes are extremely important.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    monitored_api = models.ForeignKey(
        "apis.MonitoredAPI",
        on_delete=models.CASCADE,
        related_name="logs"
    )

    status_code = models.IntegerField()

    response_time_ms = models.IntegerField(
        help_text="Response latency in milliseconds"
    )

    is_success = models.BooleanField(default=False)

    error_message = models.TextField(
        null=True,
        blank=True
    )

    checked_at = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        ordering = ["-checked_at"]

        indexes = [
            models.Index(fields=["monitored_api"]),
            models.Index(fields=["checked_at"]),
            models.Index(fields=["monitored_api", "checked_at"]),
        ]

    def __str__(self):
        return f"{self.monitored_api} | {self.status_code} | {self.response_time_ms}ms"