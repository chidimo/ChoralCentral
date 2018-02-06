"""admin"""

from django.contrib import admin
from .models import VocalPart, ScoreNotation, Score, Midi, VideoLink

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'part')

class MidiAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'part')
    raw_id_fields = ("song",)

admin.site.register(VocalPart)
admin.site.register(ScoreNotation)
admin.site.register(Score, ScoreAdmin)
admin.site.register(VideoLink)
admin.site.register(Midi, MidiAdmin)
