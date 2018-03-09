"""Request Model"""

from django.db import models
from django.urls import reverse
from django.utils import timezone

from siteuser.models import SiteUser
from song.models import Song

from universal.models import TimeStampedModel
from universal.fields import 

class Request(TimeStampedModel):
    originator = models.ForeignKey(SiteUser, null=True, on_delete=models.SET_NULL)
    request = models.CharField(max_length=200)
    slug = AutoSlugField(set_using="request")
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created", "status"]

    def __str__(self):
        return self.request

    def get_absolute_url(self):
        return reverse("request:detail", args=[str(self.id), str(self.slug)])

class Reply(TimeStampedModel):
    originator = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    song = models.OneToOneField(Song, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["request"] # change to date

    def __str__(self):
        return self.request.request

    def get_absolute_url(self):
        return reverse("request:detail", kwargs={'pk' : self.request.pk, 'slug' : self.request.slug})
