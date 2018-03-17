"""Admin"""

from django.contrib import admin

from .models import Voicing, Language, Season, MassPart, Song

class VoicingAdmin(admin.ModelAdmin):
    list_display = ("voicing", )

class LanguageAdmin(admin.ModelAdmin):
    list_display = ("language", )

class SongAdmin(admin.ModelAdmin):
    list_display = (
        "title", "like_count", "song_likers", "all_authors", "all_seasons", "all_masspart",
        "originator", "publish", "voicing", "scripture_reference", "language")
    list_filter = ("seasons", "mass_parts")
    list_editable = ("publish", )
    filter_horizontal = ("seasons", "mass_parts")
    search_fields = ("title", )

    def all_seasons(self, obj):
        return ", ".join(["{}".format(season.season) for season in obj.seasons.all()])

    def all_masspart(self, obj):
        return ", ".join(["{}".format(part.part) for part in obj.mass_parts.all()])

    def song_likers(self, obj):
        return ", ".join([each.screen_name for each in obj.likes.all()])

admin.site.register(Voicing, VoicingAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Season)
admin.site.register(MassPart)
admin.site.register(Song, SongAdmin)
