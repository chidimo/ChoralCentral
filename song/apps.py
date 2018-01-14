from django.apps import AppConfig
import algoliasearch_django as algoliasearch

from .index import SongIndex

class SongConfig(AppConfig):
    name = 'song'

    def ready(self):
        song = self.get_model("song")
        algoliasearch.register(song, SongIndex)
