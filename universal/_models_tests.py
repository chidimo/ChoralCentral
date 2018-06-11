# MODELS FOR TESTING CUSTOM FIELDS.
from django.db import models
from .fields import AutoSlugField, AutoMultipleSlugField

class AutoSlug(models.Model):
    name = models.CharField(max_length=60)
    slug = AutoSlugField(set_using='name')

    def __str__(self):
        return self.name

    def set_once_value(self):
        return self._meta.get_field("slug").set_once

class AutoSlugSetOnceFalse(models.Model):
    name = models.CharField(max_length=60)
    slug = AutoSlugField(set_using="name", set_once=False, editable=True)

    def __str__(self):
        return self.name

    def set_once_value(self):
        return self._meta.get_field("slug").set_once

class AutoSlugWithBlankSetUsing(models.Model):
    name = models.CharField(max_length=60, blank=True)
    slug = AutoSlugField(set_using='name')

class AutoMultipleSlug(models.Model):
    name = models.CharField(max_length=60)
    url = models.URLField()
    slug = AutoMultipleSlugField(set_using=["name", "url"])

class AutoMultipleSlugSetOnceFalse(models.Model):
    name = models.CharField(max_length=60)
    url = models.URLField()
    slug = AutoMultipleSlugField(set_using=["name", "url"], set_once=False)

class AutoMultipleSlugWithBlankSetUsing(models.Model):
    name = models.CharField(max_length=60, blank=True)
    url = models.URLField(blank=True)
    slug = AutoMultipleSlugField(set_using=["name", "url"])

class BT(models.Model):
    name = models.CharField(max_length=60)
    url = models.URLField()
    slug = AutoMultipleSlugField(set_using=["name"])
