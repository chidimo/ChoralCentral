import os
import glob

from django.conf import settings
from django.core.management.base import BaseCommand

from song_media.models import Midi

class Command(BaseCommand):
    help = 'Clear pdf midis without corresponding objects in the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Midi cleanup started'))

        midi_folder = os.path.join(settings.MEDIA_ROOT, 'midis')
        mid_files = [each.replace('\\', '/') for each in glob.glob("media/midis/*.mid".format(midi_folder))]
        mp3_files = [each.replace('\\', '/') for each in glob.glob("media/midis/*.mp3".format(midi_folder))]
        midi_files = [each.replace('\\', '/') for each in glob.glob("media/midis/*.midi".format(midi_folder))]

        files = mid_files + mp3_files + midi_files
        midis = [midi.media_file.url for midi in Midi.objects.all()]

        for midi in files:
            if '/{}'.format(midi) in midis:
                self.stdout.write(self.style.SUCCESS('Keep: Object exists for {}'.format(midi)))
            else:
                self.stdout.write(self.style.NOTICE('Delete: No object for {}'.format(midi)))
                os.remove(midi)
        self.stdout.write(self.style.SUCCESS('Midi cleanup completed successfully'))
