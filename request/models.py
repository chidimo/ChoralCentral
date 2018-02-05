"""Request Model"""

from django.db import models
from django.urls import reverse
from django.utils import timezone

from siteuser.models import SiteUser
from song.models import Song

from universal import models as mdl
from universal import fields as fdl

class Request(mdl.TimeStampedModel):
    MT = "MET"
    UM = "UNMET"
    FULFIL_CHOICES = (
        (MT, "Met"),
        (UM, "Unmet")
    )
    originator = models.ForeignKey(SiteUser, null=True, on_delete=models.SET_NULL)
    request = models.CharField(max_length=200)
    slug = fdl.AutoSlugField(set_using="request")
    status = models.CharField(max_length=15, choices=FULFIL_CHOICES, default="UNMET")

    class Meta:
        ordering = ["-created", "status"]

    def __str__(self):
        return self.request

    def get_absolute_url(self):
        return reverse("request:detail", args=[str(self.id), str(self.slug)])

class Reply(mdl.TimeStampedModel):
    originator = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    song = models.OneToOneField(Song, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["request"] # change to date

    def __str__(self):
        return self.request.request

    def get_absolute_url(self):
        return reverse("request:index")
