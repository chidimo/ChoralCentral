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
    creator = models.ForeignKey(SiteUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    body = models.TextField()
    slug = AutoSlugField(set_using="title")
    song = models.ForeignKey(Song, on_delete=models.SET_NULL, blank=True, null=True)
    publish = models.BooleanField(default=False)
    views = models.IntegerField(default=1)
    likes = models.ManyToManyField(SiteUser, related_name="post_likes", blank=True)
    like_count = models.IntegerField(default=0)

    class Meta:
        ordering = ('-like_count', '-created', 'title')

    def get_absolute_url(self):
        return reverse('blog:detail', args=[str(self.id), str(self.slug)])

    def __str__(self):
        return self.title

    def likers(self):
        return ", ".join([each.screen_name for each in self.likes.all()])

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
        ordering = ('-like_count', 'created',)

    def get_absolute_url(self):
        return reverse('blog:detail', args=[str(self.post.id), str(self.post.slug)])

    def __str__(self):
        return self.comment

    def save(self, *args, **kwargs):
        if self.id:
            self.like_count = self.likes.count()
        return super(Comment, self).save(*args, **kwargs)
