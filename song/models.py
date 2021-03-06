"""Models"""
import os
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
        return reverse('song:song_index')

class Language(TimeStampedModel):
    name = models.CharField(max_length=25, unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('song:song_index')

class Season(TimeStampedModel):
    name = models.CharField(max_length=15, unique=True)
    about = models.CharField(max_length=200, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('song:song_index')

    def __str__(self):
        return self.name

class MassPart(TimeStampedModel):
    name = models.CharField(max_length=15, unique=True)
    about = models.CharField(max_length=200, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('song:song_index')

    def __str__(self):
        return self.name

class Song(TimeStampedModel):
    creator         = models.ForeignKey(SiteUser, on_delete=models.SET_DEFAULT, default=1)
    voicing         = models.ForeignKey(Voicing, on_delete=models.CASCADE)
    language        = models.ForeignKey(Language, on_delete=models.CASCADE)
    publish         = models.BooleanField(default=False)

    title           = models.CharField(max_length=100)
    year            = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1000), MaxValueValidator(datetime.now().year)])
    slug            = AutoSlugField(set_using="title", set_once=False, max_length=255)

    lyrics          = models.TextField(blank=True)

    scripture_reference   = models.CharField(max_length=25, blank=True)

    tempo           = models.IntegerField(null=True, blank=True)
    bpm             = models.IntegerField(null=True, blank=True)
    divisions       = models.IntegerField(null=True, blank=True)
    tempo_text      = models.CharField(max_length=30, blank=True)
    views           = models.IntegerField(default=0)

    likes           = models.ManyToManyField(SiteUser, related_name='song_likes')
    like_count      = models.IntegerField(default=0)

    ocassion        = models.CharField(max_length=30)
    genre           = models.CharField(max_length=30)

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
        return "https://www.choralcentral.net" + reverse('song:detail', kwargs={'pk' : self.pk, 'slug' : self.slug})


    @property
    def titled_title(self):
        return self.title.title() + "whaterver"

    def __str__(self):
        return self.title.title()

    def all_authors(self):
        names = ["{} {}".format(author.first_name, author.last_name) for author in self.authors.all()]
        return ", ".join(names)

    def algolia_index_this(self):
        """Set which objects are indexed by Algolia"""
        return self.publish & (os.environ['DJANGO_SETTINGS_MODULE'] == 'choralcentral.settings.prod')

    def save(self, *args, **kwargs):
        if self.pk:
            self.like_count = self.likes.count()
        self.tempo_text = get_tempo_text(self.tempo)
        return super().save(*args, **kwargs)
