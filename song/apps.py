from django.apps import AppConfig
import algoliasearch_django as algoliasearch

from django.conf import settings

from .index import SongIndex

DJANGO_SETTINGS_MODULE = getattr(settings, 'DJANGO_SETTINGS_MODULE', None)

import os

print(os.environ['DJANGO_SETTINGS_MODULE'])

print('SETTINGS: ', DJANGO_SETTINGS_MODULE)

class SongConfig(AppConfig):
    name = 'song'

    def ready(self):
        import song.signals
        song = self.get_model("song")
        algoliasearch.register(song, SongIndex)
