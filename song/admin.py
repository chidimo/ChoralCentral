"""Docstring"""

from django.contrib import admin

from .models import Song

class SongAdmin(admin.ModelAdmin):
    list_display = ("title", "all_authors", "all_seasons", "all_masspart", "originator", "status", "voicing", "scripture_ref", "language")
    # list_filter = ("title", "likes", "seasons", "mass_parts")
    list_editable = ("status",)
    filter_horizontal = ("seasons", "mass_parts")
    search_fields = ("title", )

admin.site.register(Song, SongAdmin)
