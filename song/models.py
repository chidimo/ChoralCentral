"""Models"""

import  datetime
from django.db import models
from django.urls import reverse

from taggit.managers import TaggableManager

from siteuser.models import SiteUser
from voicing.models import Voicing
from language.models import Language
from author.models import Author
from season.models import Season
from masspart.models import MassPart

from universal import models as mdl
from universal import fields as fdl

class PublishedManager(models.Manager):
    """Return songs with 'published' marked 'True' """
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(publish=True)

class Song(mdl.TimeStampedModel):
    DR = "DRAFT"
    PB = "PUBLISHED"
    STATUS_CHOICES = (
        (DR, "Draft"),
        (PB, "Published")
    )
    originator      = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    voicing         = models.ForeignKey(Voicing, on_delete=models.CASCADE)
    language        = models.ForeignKey(Language, on_delete=models.CASCADE)
    # status          = models.CharField(max_length=12, choices=STATUS_CHOICES, default="DRAFT")
    publish         = models.BooleanField(default=False)

    title           = models.CharField(max_length=100)
    compose_date    = models.DateField(null=True, blank=True)
    likes           = models.ManyToManyField(SiteUser, related_name="song_likes")
    slug            = fdl.AutoSlugField(set_using="title")

    lyrics          = models.TextField(blank=True)
    first_line      = models.CharField(max_length=100, blank=True)

    scripture_ref   = models.CharField(max_length=25, blank=True)

    tempo           = models.IntegerField(null=True, blank=True)
    bpm             = models.IntegerField(null=True, blank=True)
    divisions       = models.IntegerField(null=True, blank=True)

    authors         = models.ManyToManyField(Author)
    seasons         = models.ManyToManyField(Season)
    mass_parts      = models.ManyToManyField(MassPart)

    objects         = models.Manager()
    published_set   = PublishedManager()

    class Meta:
        ordering = ["-created", "publish"]

    @property
    def object_id(self):
        return str(self.pk)

    @property
    def song_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('song:detail', args=[str(self.id), str(self.slug)])

    def __str__(self):
        return self.title

    @property
    def all_authors(self):
        names = ["{} {}".format(author.first_name, author.last_name) for author in self.authors.all()]
        return ", ".join(names)

    @property
    def all_seasons(self):
        return ", ".join(["{}".format(season.season) for season in self.seasons.all()])

    @property
    def all_masspart(self):
        return ", ".join(["{}".format(part.part) for part in self.mass_parts.all()])

    @property
    def tempo_text(self):
        if not self.tempo:
            return
        if self.tempo <= 25:
            return "Larghissimo"
        elif 40 <= self.tempo <= 45:
            return "Grave"
        elif 46 <= self.tempo <= 50:
            return "Largo"
        elif 51 <= self.tempo <= 60:
            return "Lento"
        elif 61 <= self.tempo <= 80:
            return "Andante"
        elif 81 <= self.tempo <= 100:
            return "Moderato"
        elif 101 <= self.tempo <= 125:
            return "Allegretto"
        elif 126 <= self.tempo <= 145:
            return "Vivace"
        elif 146 <= self.tempo <= 200:
            return "Presto"
        else:
            return "Prestissimo"
