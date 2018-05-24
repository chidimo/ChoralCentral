from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.management.base import BaseCommand

from song_media.models import Score

from google_api.api_calls import (
    create_song_folder, upload_pdf_to_drive, share_file_permission,
)

class Command(BaseCommand):
    help = 'Backup scores to google drive'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Score backup started'))

        for score in Score.objects.all():
            if (score.drive_view_link is None) or (score.drive_view_link == ""):
                self.stdout.write(self.style.SUCCESS('Backing up {}'.format(score.__str__())))
                song = score.song
                notation = score.notation
                part = score.part
                file_path = settings.BASE_DIR + score.media_file.url

                # get or create drive folder
                folder_id = song.drive_folder_id
                if (folder_id is None) or (folder_id == ""):
                    folder_name = "{}-{}".format(song.pk, slugify(song.title))
                    folder_id = create_song_folder(folder_name)
                    song.drive_folder_id = folder_id
                    song.save(update_fields=['drive_folder_id'])

                score_metadata = {}
                score_metadata['parents'] = [folder_id]
                score_metadata['name'] = file_path.rsplit('/')[-1]
                score_metadata['description'] = "{}, {} {}".format(song.title, notation.name, part.name)
                score_metadata['viewersCanCopyContent'] = True

                file_resource = upload_pdf_to_drive(score_metadata, file_path)

                score.drive_view_link = file_resource.get('webViewLink')
                score.drive_download_link = file_resource.get('webContentLink')
                score.embed_link = file_resource.get('webViewLink').replace('view?usp=drivesdk', 'preview')
                score.save(update_fields=['drive_view_link', 'drive_download_link', 'embed_link'])
                share_file_permission(file_resource.get('id')) # make shareable
            else:
                self.stdout.write(self.style.NOTICE('{} already backed up. Continue'.format(score.__str__())))
                continue
        self.stdout.write(self.style.SUCCESS('Score backup completed successfully'))
