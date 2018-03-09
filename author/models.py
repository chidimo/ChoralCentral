from django.db import models
from django.shortcuts import reverse
from siteuser.models import SiteUser

from universal import models as mdl
from universal import fields as fdl

class Author(mdl.TimeStampedModel):
    LY = 'LYRICIST'
    CP = 'COMPOSER'
    CHOICES = (('', 'Select author type'),
               (LY, 'Lyricist'),
               (CP, 'Composer'))

    originator = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    bio = models.TextField(blank=True, null=True)
    slug = fdl.AutoMultipleSlugField(set_using=["last_name", "first_name"])
    likes = models.ManyToManyField(SiteUser, related_name="author_likes")
    author_type = models.CharField(choices=CHOICES, max_length=15, default="COMPOSER")
    objects = models.Manager()

    class Meta:
        ordering = ["first_name"]

    def get_absolute_url(self):
        return reverse('author:detail', args=[str(self.id), str(self.slug)])

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
