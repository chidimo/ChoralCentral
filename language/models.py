from django.db import models

from siteuser.models import SiteUser

from universal.models import TimeStampedModel

class Language(TimeStampedModel):
    originator = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    language = models.CharField(max_length=25, unique=True)
 
    def __str__(self):
        return self.language

    def get_absolute_url(self):
        return reverse('song:index')
