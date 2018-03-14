"""Models"""

import  datetime
from django.db import models
from django.shortcuts import reverse

from taggit.managers import TaggableManager

from author.models import Author
from siteuser.models import SiteUser

from language.models import Language
from season.models import Season
from masspart.models import MassPart

from universal.models import TimeStampedModel
from universal.fields import AutoSlugField
from universal.utils import get_tempo_text

class Voicing(TimeStampedModel):
    voicing = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.voicing

    def get_absolute_url(self):
        return reverse('song:index')

class Song(TimeStampedModel):
    originator      = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    voicing         = models.ForeignKey(Voicing, on_delete=models.CASCADE)
    language        = models.ForeignKey(Language, on_delete=models.CASCADE)
    publish         = models.BooleanField(default=False)

    title           = models.CharField(max_length=100)
    compose_date    = models.DateField(null=True, blank=True)
    likes           = models.ManyToManyField(SiteUser, related_name="song_likes")
    slug            = AutoSlugField(set_using="title", max_length=255)

    lyrics          = models.TextField(blank=True)
    first_line      = models.CharField(max_length=100, blank=True)

    scripture_reference   = models.CharField(max_length=25, blank=True)

    tempo           = models.IntegerField(null=True, blank=True)
    tempo_text      = models.CharField(max_length=30, blank=True)
    bpm             = models.IntegerField(null=True, blank=True)
    divisions       = models.IntegerField(null=True, blank=True)
    views           = models.IntegerField(default=1)
    like_count      = models.IntegerField(default=1)

    authors         = models.ManyToManyField(Author)
    seasons         = models.ManyToManyField(Season)
    mass_parts      = models.ManyToManyField(MassPart)

    class Meta:
        ordering = ("-like_count", "title", "-created", "publish", 'tempo_text')

    def get_absolute_url(self):
        return reverse('song:detail', args=[str(self.id), str(self.slug)])

    def __str__(self):
        return self.title

    def all_authors(self):
        names = ["{} {}".format(author.first_name, author.last_name) for author in self.authors.all()]
        return ", ".join(names)

    def all_seasons(self):
        return ", ".join(["{}".format(season.season) for season in self.seasons.all()])

    def all_masspart(self):
        return ", ".join(["{}".format(part.part) for part in self.mass_parts.all()])

    def save(self, *args, **kwargs):
        self.tempo_text = get_tempo_text(self.tempo)
        if self.id:
            self.like_count = self.likes.count()
        return super(Song, self).save(*args, **kwargs)
