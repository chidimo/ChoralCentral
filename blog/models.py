"""Post Model"""

import datetime
from django.db import models
from django.utils import timezone
from django.urls import reverse

from universal.models import TimeStampedModel
from universal.fields import AutoSlugField

from siteuser.models import SiteUser
from song.models import Song

class Post(TimeStampedModel):
    creator = models.ForeignKey(SiteUser, on_delete=models.SET_DEFAULT, default=1)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    body = models.TextField()
    slug = AutoSlugField(set_using="title", set_once=False)
    song = models.ForeignKey(Song, on_delete=models.SET_NULL, blank=True, null=True)
    publish = models.BooleanField(default=False)
    likes = models.ManyToManyField(SiteUser, related_name='post_likes')
    like_count = models.IntegerField(default=0)

    class Meta:
        ordering = ('-like_count', '-created', 'title')

    def get_absolute_url(self):
        return #everse('blog:detail', args=[str(self.id), str(self.slug)])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk:
            self.like_count = self.likes.count()
        return super().save(*args, **kwargs)
