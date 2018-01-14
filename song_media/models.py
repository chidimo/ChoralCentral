from django.db import models
from django.shortcuts import reverse

from song.models import Song
from siteuser.models import SiteUser

from universal import models as mdl
from universal import fields as fdl

from utils import upload_pdf, upload_midi

class Sheet(mdl.TimeStampedModel):
    CH = 'CHOIR'
    SO = 'SOPRANO'
    AL = 'ALTO'
    TE = 'TENOR'
    BA = 'BASS'

    SF = "SOLFA"
    ST = "STAFF"
    LD = "LEAD"
    OT = "OTHER"

    PART_CHOICES = (
        ("", "Select Part"),
        (CH, 'Choir'),
        (SO, 'Soprano'),
        (AL, 'Alto'),
        (TE, 'Tenor'),
        (BA, 'Bass'),)

    NOTATION_CHOICES = (
        ("", "Select notation type"),
        (SF, "Solfa"),
        (ST, "Staff"),
        (LD, "Lead"),
        (OT, "Other"),)

    uploader = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_pdf)
    part = models.CharField(max_length=10, choices=PART_CHOICES)
    likes = models.ManyToManyField(SiteUser, related_name="sheet_likes")
    notation = models.CharField(max_length=8, choices=NOTATION_CHOICES)

    @property
    def sheet_likes(self):
        return self.likes.count()

    def template_name(self):
        return self.filename().split('.')[0]

    def __str__(self):
        return "{}_sheet_{}".format(self.song.title, self.part.lower())

    def get_absolute_url(self):
        return reverse('song:detail', args=[str(self.song.id), str(self.song.slug)])

class Midi(mdl.TimeStampedModel):
    CH = 'CHOIR'
    SO = 'SOPRANO'
    AL = 'ALTO'
    TE = 'TENOR'
    BA = 'BASS'

    PART_CHOICES = (
        ("", "Select Part"),
        (CH, 'Choir'),
        (SO, 'Soprano'),
        (AL, 'Alto'),
        (TE, 'Tenor'),
        (BA, 'Bass'))
    uploader = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    part = models.CharField(max_length=10, choices=PART_CHOICES)
    file = models.FileField(upload_to=upload_midi)

    def __str__(self):
        return "{}_{}_{}".format(self.song.title, self.pk, self.part)

    def template_name(self):
        return "{}_{}".format(os.path.basename(self.file.name), self.part.lower())

    def get_absolute_url(self):
        return reverse('song:detail', args=[str(self.song.id), str(self.song.slug)])

class VideoLink(mdl.TimeStampedModel):
    uploader = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    video_link = models.URLField(max_length=150, unique=True)

    def get_absolute_url(self):
        return reverse('song:detail', args=[str(self.song.id), str(self.song.slug)])

    def __str__(self):
        return "{}_{}_by_{}".format(self.song.title, self.pk, self.uploader.username)

