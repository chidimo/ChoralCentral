import os
from django.db import models
from django.shortcuts import reverse

from song.models import Song
from siteuser.models import SiteUser

from universal import models as mdl

from utils import upload_pdf, upload_midi

class VocalPart(mdl.TimeStampedModel):
    name = models.CharField(max_length=30, default='Choir', unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse()


    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(VocalPart, self).save(*args, **kwargs)

class ScoreNotation(mdl.TimeStampedModel):
    name = models.CharField(max_length=30, default='Solfa', unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse()

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(ScoreNotation, self).save(*args, **kwargs)

class Score(mdl.TimeStampedModel):
    uploader = models.ForeignKey(SiteUser, null=True, on_delete=models.SET_NULL)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    part = models.ManyToManyField(VocalPart)
    notation = models.ManyToManyField(ScoreNotation)
    likes = models.ManyToManyField(SiteUser, related_name="score_likes")
    file = models.FileField(upload_to=upload_pdf)

    class Meta:
        ordering = ('-created', )

    @property
    def score_parts(self):
        return ", ".join([each.name for each in self.part.all()])

    @property
    def score_notations(self):
        return ", ".join([each.name for each in self.notation.all()])

    @property
    def score_likes(self):
        return self.likes.count()

    def template_name(self):
        return self.filename().split('.')[0]

    def __str__(self):
        return "{}_score_{}".format(self.song.title, self.part.lower())

    def get_absolute_url(self):
        return reverse('song:detail', args=[str(self.song.id), str(self.song.slug)])

class Midi(mdl.TimeStampedModel):
    uploader = models.ForeignKey(SiteUser, null=True, on_delete=models.SET_NULL)
    song = models.ForeignKey(Song, null=True, on_delete=models.SET_NULL)
    part = models.ManyToManyField(VocalPart)
    file = models.FileField(upload_to=upload_midi)

    class Meta:
        ordering = ('-created', )

    @property
    def midi_parts(self):
        return ", ".join([each.name for each in self.part.all()])

    def __str__(self):
        return "{}_{}_{} midi".format(self.song.title, self.pk, self.part)

    @property
    def template_name(self):
        return "{}_{}".format(os.path.basename(self.file.name), self.part.lower())

    def get_absolute_url(self):
        return reverse('song:detail', args=[str(self.song.id), str(self.song.slug)])

class VideoLink(mdl.TimeStampedModel):
    uploader = models.ForeignKey(SiteUser, null=True, on_delete=models.SET_NULL)
    song = models.ForeignKey(Song, null=True, on_delete=models.SET_NULL)
    video_link = models.URLField(max_length=250, unique=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return "{}_{}_by_{}".format(self.song.title, self.pk, self.uploader.username)

    def get_absolute_url(self):
        return reverse('song:detail', args=[str(self.song.id), str(self.song.slug)])

