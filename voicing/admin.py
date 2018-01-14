"""admin"""

from django.contrib import admin
from .models import Voicing

class VoicingAdmin(admin.ModelAdmin):
    list_display = ("voicing", "originator")

admin.site.register(Voicing, VoicingAdmin)
