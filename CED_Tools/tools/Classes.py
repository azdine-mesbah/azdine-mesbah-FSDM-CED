from django.db import models
from softdelete.models import SoftDeleteObject

class TimeStampedModel(SoftDeleteObject):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    """
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)