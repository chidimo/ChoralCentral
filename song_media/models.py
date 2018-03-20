import os
from django.db import models
from django.shortcuts import reverse

from song.models import Song
from siteuser.models import SiteUser

from universal.models import TimeStampedModel
from universal.media_handlers import upload_pdf, upload_midi

class VocalPart(TimeStampedModel):
    name = models.CharField(max_length=30, default='Choir', unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse()

class ScoreNotation(TimeStampedModel):
    name = models.CharField(max_length=30, default='Solfa', unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse()

class Score(TimeStampedModel):
    uploader = models.ForeignKey(SiteUser, null=True, on_delete=models.SET_NULL)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    part = models.ForeignKey(VocalPart, on_delete=models.CASCADE)
    notation = models.ForeignKey(ScoreNotation, on_delete=models.CASCADE)
    likes = models.ManyToManyField(SiteUser, related_name="score_likes")
    downloads = models.IntegerField(default=0)
    media_file = models.FileField(upload_to=upload_pdf)

    class Meta:
        ordering = ('-downloads', 'created', )

    @property
    def score_likes(self):
        return self.likes.count()

    def __str__(self):
        return "{}-{}-{}".format(self.song.title, self.part, self.notation)

    def get_absolute_url(self):
        return reverse('song:detail', kwargs={'pk' : (self.song.id), 'slug' : self.song.slug})

class Midi(TimeStampedModel):
    uploader = models.ForeignKey(SiteUser, null=True, on_delete=models.SET_NULL)
    song = models.ForeignKey(Song, null=True, on_delete=models.SET_NULL)
    part = models.ForeignKey(VocalPart, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=True, null=True)
    likes = models.ManyToManyField(SiteUser, related_name="midi_likes")
    downloads = models.IntegerField(default=0)
    media_file = models.FileField(upload_to=upload_midi)

    class Meta:
        ordering = ('-downloads', 'created', )

    @property
    def midi_likes(self):
        return self.likes.count()

    def __str__(self):
        return "{}_{}_{} midi".format(self.song.title, self.pk, self.part)

    def get_absolute_url(self):
        return reverse('song:detail', kwargs={'pk' : (self.song.id), 'slug' : self.song.slug})

class VideoLink(TimeStampedModel):
    uploader = models.ForeignKey(SiteUser, null=True, on_delete=models.SET_NULL)
    song = models.ForeignKey(Song, null=True, on_delete=models.SET_NULL)
    video_link = models.URLField(max_length=250, unique=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return "{}_{}_by_{}".format(self.song.title, self.pk, self.uploader.username)

    def get_absolute_url(self):
        return reverse('song:detail', args=[str(self.song.id), str(self.song.slug)])

