"""Post Model"""

import datetime
from django.db import models
from django.utils import timezone
from django.urls import reverse

from taggit.managers import TaggableManager

from universal.models import TimeStampedModel
from universal.fields import 

from siteuser.models import SiteUser
from song.models import Song

class PublishedManager(models.Manager):
    """Return songs with 'published'"""
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(publish=True)

class Post(TimeStampedModel):
    creator = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    body = models.TextField()
    slug = AutoSlugField(set_using="title")
    song = models.ForeignKey(Song, on_delete=models.SET_NULL, blank=True, null=True)
    publish = models.BooleanField(default=False)
    views = models.IntegerField(default=1)
    likes = models.ManyToManyField(SiteUser, related_name="post_likes", blank=True)
    like_count = models.IntegerField(default=0)

    objects = models.Manager()
    published_set = PublishedManager()

    class Meta:
        ordering = ('-like_count', '-created', 'title')

    def get_absolute_url(self):
        return reverse('blog:detail', args=[str(self.id), str(self.slug)])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.id:
            self.like_count = self.likes.count()
        return super(Post, self).save(*args, **kwargs)

class Comment(TimeStampedModel):
    creator = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.ManyToManyField(SiteUser, related_name="comment_likes", blank=True)
    like_count = models.IntegerField(default=1)
    comment = models.TextField()

    class Meta:
        ordering = ('-like_count', '-created',)

    def get_absolute_url(self):
        return reverse('blog:detail', args=[str(self.post.id), str(self.post.slug)])

    def __str__(self):
        return self.comment

    def save(self, *args, **kwargs):
        if self.id:
            self.like_count = self.likes.count()
        return super(Comment, self).save(*args, **kwargs)
