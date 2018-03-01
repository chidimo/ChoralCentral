"""Post Model"""

import datetime
from django.db import models
from django.utils import timezone
from django.urls import reverse

from taggit.managers import TaggableManager

from universal import models as mdl
from universal import fields as fdl

from siteuser.models import SiteUser
from song.models import Song

class PublishedManager(models.Manager):
    """Return songs with 'published'"""
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(publish=True)

class Post(mdl.TimeStampedModel):
    creator = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    body = models.TextField()
    slug = fdl.AutoSlugField(set_using="title")
    song = models.ForeignKey(Song, on_delete=models.CASCADE, blank=True, null=True)
    publish = models.BooleanField(default=False)
    likes = models.ManyToManyField(SiteUser, related_name="post_likes", blank=True)
    like_count = models.IntegerField(default=1)

    published_set = PublishedManager()
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('blog:detail', args=[str(self.id), str(self.slug)])

    def __str__(self):
        return self.title

class Comment(mdl.TimeStampedModel):
    creator = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.ManyToManyField(SiteUser, related_name="comment_likes", blank=True)
    like_count = models.IntegerField(default=1)
    comment = models.TextField()

    def get_absolute_url(self):
        return reverse('blog:detail', args=[str(self.post.id), str(self.post.slug)])

    def __str__(self):
        return self.comment
