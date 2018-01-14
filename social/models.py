from django.db import models
from django.utils import timezone

from siteuser.models import SiteUser
from song.models import Song

from universal import models as mdl


class Favorite(mdl.TimeStampedModel):
    favoriter = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    song = models.ManyToManyField(Song)

    def __str__(self):
        return "{}'s favorites".format(self.favoriter.screen_name)

class Collection(mdl.TimeStampedModel):
    collector = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    song = models.ManyToManyField(Song)

    def __str__(self):
        return "{}'s collection".format(self.collector.screen_name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        super(Collection, self).save(*args, **kwargs)


