"""Models"""

from datetime import datetime

from django.db import models
from django.shortcuts import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

from author.models import Author
from siteuser.models import SiteUser

from universal.models import TimeStampedModel
from universal.fields import AutoSlugField
from .utils import get_tempo_text

class Voicing(TimeStampedModel):
    name = models.CharField(max_length=10, unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('song:index')

class Language(TimeStampedModel):
    name = models.CharField(max_length=25, unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('song:index')

class Season(TimeStampedModel):
    SEASON_CHOICES = (
        ("", "Select a season"),
        ("ordinary time", "Ordinary Time"),
        ("advent", "Advent"),
        ("christmas", "Christmas"),
        ("lent", "Lent"),
        ("easter", "Easter"),
        ("pentecost", "Pentecost"),
        ('any', "Any"),
        ("na", "NA"),
    )
    name = models.CharField(max_length=15, choices=SEASON_CHOICES, unique=True)
    about = models.CharField(max_length=200, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('song:index')

    def __str__(self):
        return self.name

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
    name = models.CharField(max_length=15, choices=PART_CHOICES, unique=True)
    about = models.CharField(max_length=200, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('song:index')

    def __str__(self):
        return self.name

class Song(TimeStampedModel):
    OCASSION_CHOICES = (
        ("", "Select ocassion"),
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
    creator      = models.ForeignKey(SiteUser, on_delete=models.SET_DEFAULT, default=1)
    voicing         = models.ForeignKey(Voicing, on_delete=models.CASCADE)
    language        = models.ForeignKey(Language, on_delete=models.CASCADE)
    publish         = models.BooleanField(default=False)

    title           = models.CharField(max_length=100)
    year            = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1000), MaxValueValidator(datetime.now().year)])
    slug            = AutoSlugField(set_using="title", max_length=255)

    lyrics          = models.TextField(blank=True)

    scripture_reference   = models.CharField(max_length=25, blank=True)

    tempo           = models.IntegerField(null=True, blank=True)
    bpm             = models.IntegerField(null=True, blank=True)
    divisions       = models.IntegerField(null=True, blank=True)
    tempo_text      = models.CharField(max_length=30, blank=True)
    views           = models.IntegerField(default=0)

    likes           = models.ManyToManyField(SiteUser, related_name='song_likes')
    like_count      = models.IntegerField(default=0)

    ocassion        = models.CharField(max_length=30, choices=OCASSION_CHOICES)
    genre           = models.CharField(max_length=30, choices=GENRE_CHOICES)

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
        self.like_count = self.likes.count()
        return super(Song, self).save(*args, **kwargs)
