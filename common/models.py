from django.db import models


class TenantAwareModel(models.Model):
    """
    Abstract base model to enforce organization ownership.
    """

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="%(class)ss"
    )

    class Meta:
        abstract = True