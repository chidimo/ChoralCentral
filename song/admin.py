"""Admin"""

from django.contrib import admin

from .models import Voicing, Language, Season, MassPart, Song

class VoicingAdmin(admin.ModelAdmin):
    list_display = ("name", )

class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", )

class SongAdmin(admin.ModelAdmin):
    list_display = (
        "title", "get_absolute_uri", "youtube_playlist_id", "drive_folder_id", "like_count", "all_authors", "all_seasons", "all_masspart",
        "creator", "publish", "voicing", "scripture_reference", "language", 'likers')
    list_filter = ("seasons", "mass_parts")
    list_editable = ("publish", )
    filter_horizontal = ("seasons", "mass_parts")
    search_fields = ("title", )

    def likers(self, obj):
        return ", ".join([each.screen_name for each in obj.likes.all()])

    def all_seasons(self, obj):
        return ", ".join(["{}".format(season.name) for season in obj.seasons.all()])

    def all_masspart(self, obj):
        return ", ".join(["{}".format(part.name) for part in obj.mass_parts.all()])

admin.site.register(Voicing, VoicingAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Season)
admin.site.register(MassPart)
admin.site.register(Song, SongAdmin)
