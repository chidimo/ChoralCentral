from django.db import models

from .utils import TimeStampedModel

class Url301(TimeStampedModel):
    old_url = models.URLField()
    new_url = models.URLField()

    class Meta:
        ordering = ('new_url', 'old_url')

    def __str__(self):
        return self.new_url
