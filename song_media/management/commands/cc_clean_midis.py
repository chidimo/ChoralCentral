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
        midi_files = [each.replace('\\', '/') for each in glob.glob("media/midis/*.pdf".format(midi_folder))]
        midis = [midi.media_file.url for midi in Midi.objects.all()]

        for midi in midi_files:
            if '/{}'.format(midi) in midis:
                self.stdout.write(self.style.SUCCESS('Cleaning started'.))
                self.stdout.write(self.style.SUCCESS('Keep: Object exists for {}'.format(midi)))
            else:
                self.stdout.write(self.style.NOTICE('Delete: No object for {}'.format(midi)))
                os.remove(midi)
        self.stdout.write(self.style.SUCCESS('Midi cleanup completed successfully'))
