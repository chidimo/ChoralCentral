from django.db import models
from django.shortcuts import reverse
from django.core.validators import RegexValidator

from siteuser.models import SiteUser

from universal.models import TimeStampedModel
from universal.fields import AutoMultipleSlugField

class Author(TimeStampedModel):
    msg = "Only alphabets are values allowed."
    validate_name = RegexValidator(regex=r'[a-zA-Z-\s]+', message=msg, code='Not set')
    CHOICES = (('', 'Select author type'),
               ('lyricist', 'Lyricist'),
               ('composer', 'Composer'),
               ('lyricist and composer', 'Lyricist and Composer'))
    originator = models.ForeignKey(SiteUser, on_delete=models.SET_DEFAULT, default=1)
    first_name = models.CharField(max_length=30, validators=[validate_name])
    last_name = models.CharField(max_length=30, validators=[validate_name])
    bio = models.TextField(blank=True, null=True)
    slug = AutoMultipleSlugField(set_using=["last_name", "first_name"], max_length=255)
    likes = models.ManyToManyField(SiteUser, related_name="author_likes")
    author_type = models.CharField(choices=CHOICES, max_length=30)

    class Meta:
        ordering = ["first_name"]

    def get_absolute_url(self):
        return reverse('author:detail', kwargs={'pk' : self.id, 'slug' : self.slug })

    def __str__(self):
        return "{} {}".format(self.first_name.title(), self.last_name.title())
