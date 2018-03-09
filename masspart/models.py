from django.db import models

from universal.models import TimeStampedModel

class MassPart(TimeStampedModel):
    EN = "ENTRANCE"
    KY = "KYRIE"
    GL = "GLORIA"
    AC = "ACCLAMATION"
    OF = "OFFERTORY"
    CM = "COMMUNION"
    SS = "SANCTUS"
    AD = "AGNUS DEI"
    RC = "RECESSION"
    GN = "GENERAL"
    CR = "CAROL"
    NA = "NA"
    PART_CHOICES = (
        ("", "Select Mass part"),
        (EN, "Entrance"),
        (KY, "Kyrie"),
        (GL, "Gloria"),
        (AC, "Acclamation"),
        (OF, "Offertory"),
        (CM, "Communion"),
        (SS, "Sanctus"),
        (AD, "Agnus Dei"),
        (RC, "Recesssion"),
        (CR, "Carol"),
        (GN, "General"),
        (NA, "NA")
    )
    part = models.CharField(max_length=15, choices=PART_CHOICES, unique=True)
    about = models.TextField()

    def get_absolute_url(self):
        return reverse('song:masspart', args=[str(self.id)])

    def __str__(self):
        return self.part
