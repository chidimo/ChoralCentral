from django.db import models
from django.shortcuts import reverse
from siteuser.models import SiteUser

from universal.models import TimeStampedModel

class Voicing(TimeStampedModel):
    voicing = models.CharField(max_length=10, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.voicing

    def get_absolute_url(self):
        return reverse('song:index')
