"""admin"""

from django.contrib import admin
from .models import VocalPart, ScoreNotation, Score, Midi, VideoLink

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'part', 'uploader', 'media_file', 'drive_view_link', 'drive_download_link', 'embed_link', 'thumbnail')

    def uploader(self, obj):
        return obj.uploader.screen_name

class MidiAdmin(admin.ModelAdmin):
    list_display = ('__str__', "fformat", 'fsize', 'part', 'uploader', 'description', 'media_file', 'drive_view_link', 'embed_link', 'drive_download_link')
    list_editable = ('fformat', )
    def uploader(self, obj):
        return obj.uploader.screen_name

class VideoLinkAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'uploader', 'youtube_likes', 'youtube_views', 'channel_link', 'video_link')

    def uploader(self, obj):
        return obj.uploader.screen_name

admin.site.register(VocalPart)
admin.site.register(ScoreNotation)
admin.site.register(Score, ScoreAdmin)
admin.site.register(VideoLink, VideoLinkAdmin)
admin.site.register(Midi, MidiAdmin)
# python manage.py migrate