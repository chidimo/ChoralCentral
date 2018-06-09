from django.apps import AppConfig


class SongMediaConfig(AppConfig):
    name = 'song_media'


    def ready(self):
        import song_media.signals
