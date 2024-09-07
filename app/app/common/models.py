import uuid

from django.db import models


class TimeStampedModel(models.Model):
    """This is a common abstract model that describe the history of an instance."""
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True, null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, auto_created=True, null=False, blank=False)

    class Meta:
        abstract = True
