"""admin"""

from django.contrib import admin
from .models import VocalPart, ScoreNotation, Score, Midi, VideoLink

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'part', 'uploader', 'media_file', )

    def uploader(self, obj):
        return obj.uploader.screen_name

class MidiAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'part', 'uploader', 'description', 'media_file', )

    def uploader(self, obj):
        return obj.uploader.screen_name

class VideoLinkAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'uploader', 'video_link')

    def uploader(self, obj):
        return obj.uploader.screen_name

admin.site.register(VocalPart)
admin.site.register(ScoreNotation)
admin.site.register(Score, ScoreAdmin)
admin.site.register(VideoLink, VideoLinkAdmin)
admin.site.register(Midi, MidiAdmin)
