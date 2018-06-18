from django.db import models

from .utils import TimeStampedModel

class Url301(TimeStampedModel):
    old_url = models.URLField()
    new_url = models.URLField()
