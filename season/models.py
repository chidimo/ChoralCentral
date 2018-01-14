from django.db import models

from universal import models as mdl

class Season(mdl.TimeStampedModel):
    OT = "ORDINARY TIME"
    AD = "ADVENT"
    CM = "CHRISTMAS"
    LT = "LENT"
    ER = "EASTER"
    PT = "PENTECOST"
    NA = "NA"
    SEASON_CHOICES = (
        ("", "Select Season"),
        (OT, "Ordinary Time"),
        (AD, "Advent"),
        (CM, "Christmas"),
        (LT, "Lent"),
        (ER, "Easter"),
        (PT, "Pentecost"),
        (NA, "NA")
    )
    season = models.CharField(max_length=15, choices=SEASON_CHOICES, unique=True)
    about = models.TextField()

    def get_absolute_url(self):
        return reverse('song:index')

    def __str__(self):
        return self.season
