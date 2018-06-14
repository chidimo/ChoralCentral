from django.apps import AppConfig
import algoliasearch_django as algoliasearch

import secretballot

from .index import SongIndex

class SongConfig(AppConfig):
    name = 'song'

    def ready(self):
        import song.signals
        song = self.get_model("song")
        algoliasearch.register(song, SongIndex)

        secretballot.enable_voting_on(song)
