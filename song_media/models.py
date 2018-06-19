from django.db import models
from django.shortcuts import reverse

from sorl.thumbnail import ImageField

from song.models import Song
from siteuser.models import SiteUser

from universal.models import TimeStampedModel
from .utils import save_score, save_score_thumbnail, save_midi, save_video_thumbnail

class VocalPart(TimeStampedModel):
    name = models.CharField(max_length=30, default='Choir', unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('song:detail', kwargs={'pk' : (self.song.id), 'slug' : self.song.slug})

class ScoreNotation(TimeStampedModel):
    name = models.CharField(max_length=30, default='Solfa', unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('song:detail', kwargs={'pk' : (self.song.id), 'slug' : self.song.slug})

class Score(TimeStampedModel):
    creator = models.ForeignKey(SiteUser, on_delete=models.SET_DEFAULT, default=1)
    song = models.ForeignKey(Song, on_delete=models.SET_NULL, null=True)
    part = models.ForeignKey(VocalPart, on_delete=models.SET_NULL, null=True)
    notation = models.ForeignKey(ScoreNotation, on_delete=models.SET_NULL, null=True)
    fsize = models.FloatField(null=True,blank=True)
    likes = models.ManyToManyField(SiteUser, related_name='score_likes')
    like_count = models.IntegerField(default=0)
    media_file = models.FileField(upload_to=save_score)
    thumbnail = models.ImageField(upload_to=save_score_thumbnail, null=True)
    downloads = models.IntegerField(default=0)
    drive_view_link = models.URLField(null=True, blank=True)
    drive_download_link = models.URLField(null=True, blank=True)
    embed_link = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ('-like_count', '-downloads', 'created', )

    def __str__(self):
        return "{}-{}-{}".format(self.song.title, self.part, self.notation)

    def get_absolute_url(self):
        return reverse('song:detail', kwargs={'pk' : self.song.id, 'slug' : self.song.slug})

    def score_download_path(self):
        return "https://www.choralcentral.net" + self.media_file.url

    def score_absolute_url(self):
        return "https://www.choralcentral.net" + reverse('song-media:score_view', kwargs={'pk' : (self.id)})

    def save(self, *args, **kwargs):
        if self.id:
            self.like_count = self.likes.count()
        return super().save(*args, **kwargs)

class Midi(TimeStampedModel):
    creator = models.ForeignKey(SiteUser, on_delete=models.SET_DEFAULT, default=1)
    song = models.ForeignKey(Song, null=True, on_delete=models.SET_NULL)
    part = models.ForeignKey(VocalPart, on_delete=models.SET_NULL, null=True)
    fformat = models.CharField(max_length=10, blank=True)
    fsize = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    likes = models.ManyToManyField(SiteUser, related_name='midi_likes')
    like_count = models.IntegerField(default=0)
    media_file = models.FileField(upload_to=save_midi, null=True, blank=True)
    downloads = models.IntegerField(default=0)
    drive_view_link = models.URLField(null=True, blank=True)
    drive_download_link = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ('-like_count', '-downloads', 'created', )

    def __str__(self):
        return "{}-{}".format(self.song.title, self.part)

    def get_absolute_url(self):
        return reverse('song:detail', kwargs={'pk' : (self.song.id), 'slug' : self.song.slug})
        
    def save(self, *args, **kwargs):
        if self.id:
            self.like_count = self.likes.count()
        return super().save(*args, **kwargs)

class VideoLink(TimeStampedModel):
    creator = models.ForeignKey(SiteUser, on_delete=models.SET_DEFAULT, default=1)
    song = models.ForeignKey(Song, null=True, on_delete=models.SET_NULL)
    video_link = models.URLField(max_length=100, unique=True)
    channel_link = models.URLField(max_length=100, default='')
    playlist = models.CharField(max_length=100, default='playlist')
    video_playlist_link = models.CharField(max_length=100, default='playlist link')
    title = models.CharField(max_length=100, default='video title')
    youtube_likes = models.IntegerField(default=0)
    youtube_views = models.IntegerField(default=0)
    thumbnail = ImageField(upload_to=save_video_thumbnail, blank=True, null=True)
    thumbnail_url = models.URLField(default='www.youtube.com')
    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.song.title

    def get_absolute_url(self):
        return reverse('song:detail', args=[str(self.song.id), str(self.song.slug)])
