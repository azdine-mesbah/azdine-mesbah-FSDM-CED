from django.db import models
from softdelete.models import SoftDeleteObject
from random import randint

class TimeStampedModel(SoftDeleteObject):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    """
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    @property
    def color(self):
        return "#{:06x}".format(randint(0, 0xFFFFFF))
