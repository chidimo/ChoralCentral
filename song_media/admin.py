"""admin"""

from django.contrib import admin
from .models import VocalPart, ScoreNotation, Score, Midi, VideoLink

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'part', 'creator', 'media_file', 'drive_view_link', 'drive_download_link', 'embed_link', 'thumbnail')

    def creator(self, obj):
        return obj.creator.screen_name

class MidiAdmin(admin.ModelAdmin):
    list_display = ('__str__', "fformat", 'fsize', 'part', 'creator', 'description', 'media_file', 'drive_view_link', 'drive_download_link')
    def creator(self, obj):
        return obj.creator.screen_name

class VideoLinkAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'creator', 'youtube_likes', 'youtube_views', 'channel_link', 'video_link')

    def creator(self, obj):
        return obj.creator.screen_name

admin.site.register(VocalPart)
admin.site.register(ScoreNotation)
admin.site.register(Score, ScoreAdmin)
admin.site.register(VideoLink, VideoLinkAdmin)
admin.site.register(Midi, MidiAdmin)
# python manage.py migrate