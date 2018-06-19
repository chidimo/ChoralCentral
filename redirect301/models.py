from django.db import models

from .utils import TimeStampedModel

class Url301(TimeStampedModel):
    app_name = models.CharField(max_length=20)
    old_reference = models.CharField(max_length=50)
    new_reference = models.CharField(max_length=50)

    class Meta:
        ordering = ('new_reference', 'old_reference')

    def __str__(self):
        return self.new_reference
