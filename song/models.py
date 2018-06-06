"""Models"""

from django.db import models
from django.shortcuts import reverse

from author.models import Author
from siteuser.models import SiteUser

from universal.models import TimeStampedModel
from universal.fields import AutoSlugField
from .utils import get_tempo_text

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
    SEASON_CHOICES = (
        ("", "Select a season"),
        ("ordinary time", "Ordinary Time"),
        ("advent", "Advent"),
        ("christmas", "Christmas"),
        ("lent", "Lent"),
        ("Easter", "Easter"),
        ("pentecost", "Pentecost"),
        ("na", "NA")
    )
    season = models.CharField(max_length=15, choices=SEASON_CHOICES, unique=True)
    about = models.TextField()

    def get_absolute_url(self):
        return reverse('song:index')

    def __str__(self):
        return self.season

class MassPart(TimeStampedModel):
    PART_CHOICES = (
        ("", "Select a mass part"),
        ("entrance", "Entrance"),
        ("kyrie", "Kyrie"),
        ("gloria", "Gloria"),
        ("acclamation", "Acclamation"),
        ("offertory", "Offertory"),
        ("communion", "Communion"),
        ("sanctus", "Sanctus"),
        ("agnus dei", "Agnus Dei"),
        ("recesssion", "Recesssion"),
        ("na", "NA")
    )
    part = models.CharField(max_length=15, choices=PART_CHOICES, unique=True)
    about = models.TextField()

    def get_absolute_url(self):
        return reverse('song:index', args=[str(self.id)])

    def __str__(self):
        return self.part

class Song(TimeStampedModel):
    SONG_TYPE_CHOICES = (
        ("sacred", "Sacred"),
        ("liturgical", "Liturgical"),
        ("secular", "Secular"),
        ("na", "NA"),
    )
    GENRE_CHOICES = (
        ("", "Select a genre"),
        ("anthem", "Anthem"),
        ("carol", "Carol"),
        ("chorus", "Chorus"),
        ("folk music", "Folk music"),
        ("gregorian chant", "Gregorian Chant"),
        ("hymn", "Hymn"),
        ("litany", "Litany"),
        ("madrigral", "Madrigal"),
        ("march", "March"),
        ("mass", "Mass"),
        ("motet", "Motet"),
        ("popular music", "Popular music"),
        ("psalm", "Psalm"),
        ("requiem", "Requiem"),
        ("sequence", "Sequence"),
        ("na", "NA"),
    )
    originator      = models.ForeignKey(SiteUser, on_delete=models.SET_NULL, null=True)
    voicing         = models.ForeignKey(Voicing, on_delete=models.CASCADE)
    language        = models.ForeignKey(Language, on_delete=models.CASCADE)
    publish         = models.BooleanField(default=False)

    title           = models.CharField(max_length=100)
    compose_date    = models.DateField(null=True, blank=True)
    likes           = models.ManyToManyField(SiteUser, related_name="song_likes")
    slug            = AutoSlugField(set_using="title", max_length=255)

    lyrics          = models.TextField(blank=True)

    scripture_reference   = models.CharField(max_length=25, blank=True)

    tempo           = models.IntegerField(null=True, blank=True)
    bpm             = models.IntegerField(null=True, blank=True)
    divisions       = models.IntegerField(null=True, blank=True)
    tempo_text      = models.CharField(max_length=30, blank=True)
    views           = models.IntegerField(default=0)
    like_count      = models.IntegerField(default=0)

    ocassion        = models.CharField(max_length=30, choices=SONG_TYPE_CHOICES, default="sacred")
    genre           = models.CharField(max_length=30, choices=GENRE_CHOICES, default="hymn")

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
        return "https://www.choralcentral.net" + reverse('song:detail', args=[str(self.id), str(self.slug)])

    def __str__(self):
        return self.title

    def all_authors(self):
        names = ["{} {}".format(author.first_name, author.last_name) for author in self.authors.all()]
        return ", ".join(names)

    def should_index(self):
        """Set which objects are indexed by Algolia"""
        return self.publish

    def save(self, *args, **kwargs):
        self.tempo_text = get_tempo_text(self.tempo)
        return super(Song, self).save(*args, **kwargs)
