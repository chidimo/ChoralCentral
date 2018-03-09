from django.db import models
from django.shortcuts import reverse
from siteuser.models import SiteUser

from universal import models as mdl

class VoicingManager(models.Manager):
    def voicing_exists(self, voicing):
        return super(VoicingManager, self).get_queryset().filter(voicing=voicing.upper()).exists()

class Voicing(mdl.TimeStampedModel):
    originator = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    voicing = models.CharField(max_length=10, unique=True)
    objects = models.Manager()
    voicings = VoicingManager()

    def __str__(self):
        return self.voicing

    def get_absolute_url(self):
        return reverse('song:index')
