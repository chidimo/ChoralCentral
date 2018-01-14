from django.db import models
from django.shortcuts import reverse

from song.models import Song
from siteuser.models import SiteUser

from universal import models as mdl

class TodayMass(mdl.TimeStampedModel):
    name = models.CharField(max_length=75)
    owner = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return "Hymns for {}".format(self.name)

    def get_abolute_url(self):
        return reverse("todaymass:mass", args=[str(self.id)])
        
