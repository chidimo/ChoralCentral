from django.db import models
from django.shortcuts import reverse
from django.core.validators import RegexValidator

from siteuser.models import SiteUser

from universal.models import TimeStampedModel
from universal.fields import AutoMultipleSlugField

class Author(TimeStampedModel):
    msg = "Only alphabetic values are allowed."
    validate_name = RegexValidator(regex=r'[a-zA-Z-\s]+', message=msg, code='Not set')
    CHOICES = (('', 'Select author type'),
               ('lyricist', 'Lyricist'),
               ('composer', 'Composer'),
               ('lyricist and composer', 'Lyricist and Composer'))
    creator = models.ForeignKey(SiteUser, on_delete=models.SET_DEFAULT, default=1)
    first_name = models.CharField(max_length=30, validators=[validate_name])
    last_name = models.CharField(max_length=30, validators=[validate_name])
    bio = models.TextField(blank=True, null=True)
    slug = AutoMultipleSlugField(set_using=["last_name", "first_name"], max_length=255)
    author_type = models.CharField(choices=CHOICES, max_length=25)

    class Meta:
        ordering = ("last_name", '-created')

    def get_absolute_url(self):
        return reverse('author:detail', kwargs={'pk' : self.pk, 'slug' : self.slug })

    def get_absolute_uri(self):
        return "https://www.choralcentral.net" + reverse('author:detail', kwargs={'pk' : self.pk, 'slug' : self.slug})

    def __str__(self):
        name = "{} {}".format(self.first_name, self.last_name)
        return name.title()
