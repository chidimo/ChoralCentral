import os
from django.apps import AppConfig
import algoliasearch_django as algoliasearch

from django.conf import settings

from .index import SongIndex

class SongConfig(AppConfig):
    name = 'song'

    def ready(self):
        import song.signals
        song = self.get_model("song")
        algoliasearch.register(song, SongIndex)
