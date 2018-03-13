"""Admin"""

from django.contrib import admin

from .models import Song

class SongAdmin(admin.ModelAdmin):
    list_display = (
        "title", "like_count", "all_authors", "all_seasons", "all_masspart",
        "originator", "publish", "voicing", "scripture_reference", "language")
    list_filter = ("seasons", "mass_parts")
    list_editable = ("publish", )
    filter_horizontal = ("seasons", "mass_parts")
    search_fields = ("title", )

admin.site.register(Song, SongAdmin)
