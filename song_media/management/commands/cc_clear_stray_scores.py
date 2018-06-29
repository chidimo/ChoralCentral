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
        pdf_scores = [each for each in glob.glob("{}/*.pdf".format(score_folder))]
        scores = [score.media_file.url for score in Score.objects.all()]

        print('pdf_scores')
        print(pdf_scores)
        print()
        print('scores')
        print(scores)

        for score in pdf_scores:
            if score in scores:
                print(score)
                self.stdout.write(self.style.SUCCESS('{} has object. Keep'.format(score)))
            else:
                self.stdout.write(self.style.NOTICE('{} has no object. Deleting'.format(score)))
                continue
        self.stdout.write(self.style.SUCCESS('Score cleanup completed successfully'))
