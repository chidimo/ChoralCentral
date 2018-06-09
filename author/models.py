from django.db import models
from django.shortcuts import reverse
from siteuser.models import SiteUser

from universal.models import TimeStampedModel
from universal.fields import AutoMultipleSlugField

class Author(TimeStampedModel):
    CHOICES = (('', 'Select author type'),
               ('lyricist', 'Lyricist'),
               ('composer', 'Composer'))

    originator = models.ForeignKey(SiteUser, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    bio = models.TextField(blank=True, null=True)
    slug = AutoMultipleSlugField(set_using=["last_name", "first_name"], max_length=255)
    likes = models.ManyToManyField(SiteUser, related_name="author_likes")
    author_type = models.CharField(choices=CHOICES, max_length=15, default="lyricist")

    class Meta:
        ordering = ["first_name"]

    def get_absolute_url(self):
        return reverse('author:detail', kwargs={'pk' : self.id, 'slug' : self.slug })

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
