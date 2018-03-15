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

admin.site.register(Voicing, VoicingAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Season)
admin.site.register(MassPart)
admin.site.register(Song, SongAdmin)
