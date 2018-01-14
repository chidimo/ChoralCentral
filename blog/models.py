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
        return super(PublishedManager, self).get_queryset().filter(status="PUBLISHED")

class Post(mdl.TimeStampedModel):
    DR = "DRAFT"
    PB = "PUBLISHED"
    STATUS_CHOICES = (
        (DR, "Draft"),
        (PB, "Published")
    )
    creator = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="DRAFT")
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    body = models.TextField()
    slug = fdl.AutoSlugField(set_using="title")
    song = models.ForeignKey(Song, on_delete=models.CASCADE, blank=True, null=True)

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
    comment = models.TextField()

    def get_absolute_url(self):
        return reverse('blog:detail', args=[str(self.post.id), str(self.post.slug)])

    def __str__(self):
        return self.comment

    @property
    def comment_likes(self):
        return self.likes.count()
