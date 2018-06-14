from django.apps import AppConfig

import secretballot

class SongMediaConfig(AppConfig):
    name = 'song_media'

    def ready(self):
        import song_media.signals
        secretballot.enable_voting_on(self.get_model('score'))
        secretballot.enable_voting_on(self.get_model('midi'))
