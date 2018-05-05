"""Models"""

import  datetime
from django.db import models
from django.shortcuts import reverse

from taggit.managers import TaggableManager

from author.models import Author
from siteuser.models import SiteUser

from universal.models import TimeStampedModel
from universal.fields import AutoSlugField
from universal.utils import get_tempo_text

class Voicing(TimeStampedModel):
    voicing = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.voicing

    def get_absolute_url(self):
        return reverse('song:index')

class Language(TimeStampedModel):
    language = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.language

    def get_absolute_url(self):
        return reverse('song:index')

class Season(TimeStampedModel):
    OT = "ORDINARY TIME"
    AD = "ADVENT"
    CM = "CHRISTMAS"
    LT = "LENT"
    ER = "EASTER"
    PT = "PENTECOST"
    NA = "NA"
    SEASON_CHOICES = (
        ("", "Select Season"),
        (OT, "Ordinary Time"),
        (AD, "Advent"),
        (CM, "Christmas"),
        (LT, "Lent"),
        (ER, "Easter"),
        (PT, "Pentecost"),
        (NA, "NA")
    )
    season = models.CharField(max_length=15, choices=SEASON_CHOICES, unique=True)
    about = models.TextField()

    def get_absolute_url(self):
        return reverse('song:index')

    def __str__(self):
        return self.season

class MassPart(TimeStampedModel):
    EN = "ENTRANCE"
    KY = "KYRIE"
    GL = "GLORIA"
    AC = "ACCLAMATION"
    OF = "OFFERTORY"
    CM = "COMMUNION"
    SS = "SANCTUS"
    AD = "AGNUS DEI"
    RC = "RECESSION"
    GN = "GENERAL"
    CR = "CAROL"
    NA = "NA"
    PART_CHOICES = (
        ("", "Select Mass part"),
        (EN, "Entrance"),
        (KY, "Kyrie"),
        (GL, "Gloria"),
        (AC, "Acclamation"),
        (OF, "Offertory"),
        (CM, "Communion"),
        (SS, "Sanctus"),
        (AD, "Agnus Dei"),
        (RC, "Recesssion"),
        (CR, "Carol"),
        (GN, "General"),
        (NA, "NA")
    )
    part = models.CharField(max_length=15, choices=PART_CHOICES, unique=True)
    about = models.TextField()

    def get_absolute_url(self):
        return reverse('song:index', args=[str(self.id)])

    def __str__(self):
        return self.part

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
    views           = models.IntegerField(default=0)
    like_count      = models.IntegerField(default=0)

    authors         = models.ManyToManyField(Author)
    seasons         = models.ManyToManyField(Season)
    mass_parts      = models.ManyToManyField(MassPart)

    youtube_playlist_id = models.CharField(max_length=100, null=True, blank=True)
    drive_folder_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ("-like_count", "title", "-created", "publish", 'tempo_text')

    def get_absolute_url(self):
        return reverse('song:detail', args=[str(self.id), str(self.slug)])

    def get_absolute_uri(self):
        return "http://www.choralcentral.net" + reverse('song:detail', args=[str(self.id), str(self.slug)])

    def __str__(self):
        return self.title

    def all_authors(self):
        names = ["{} {}".format(author.first_name, author.last_name) for author in self.authors.all()]
        return ", ".join(names)

    def save(self, *args, **kwargs):
        self.tempo_text = get_tempo_text(self.tempo)
        return super(Song, self).save(*args, **kwargs)
