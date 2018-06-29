import os
import glob

from django.conf import settings
from django.core.management.base import BaseCommand

from song_media.models import Score

class Command(BaseCommand):
    help = 'Clear pdf scores without corresponding objects in the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Score cleanup started'))

        score_folder = os.path.join(settings.MEDIA_ROOT, 'scores')
        pdf_files = [each.replace('\\', '/') for each in glob.glob("media/scores/*.pdf".format(score_folder))]
        scores = [score.media_file.url for score in Score.objects.all()]

        for score in pdf_files:
            if '/{}'.format(score) in scores:
                self.stdout.write(self.style.SUCCESS('Cleaning started'.))
                self.stdout.write(self.style.SUCCESS('Keep: Object exists for {}'.format(score)))
            else:
                self.stdout.write(self.style.NOTICE('Delete: No object for {}'.format(score)))
                os.remove(score)
        self.stdout.write(self.style.SUCCESS('Score cleanup completed successfully'))
