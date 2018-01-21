"""admin"""

from django.contrib import admin
from .models import VocalPart, ScoreNotation, Score, Midi, VideoLink

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'score_notations', 'score_parts')

class MidiAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'midi_parts')
    raw_id_fields = ("song",)

admin.site.register(VocalPart)
admin.site.register(ScoreNotation)
admin.site.register(Score, ScoreAdmin)
admin.site.register(VideoLink)
admin.site.register(Midi, MidiAdmin)
