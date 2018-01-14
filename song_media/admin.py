"""admin"""

from django.contrib import admin
from .models import Sheet, Midi, VideoLink

class MidiAdmin(admin.ModelAdmin):
    raw_id_fields = ("song",)

admin.site.register(Sheet)
admin.site.register(VideoLink)
admin.site.register(Midi, MidiAdmin)
