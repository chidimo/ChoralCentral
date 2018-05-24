from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.management.base import BaseCommand

from song_media.models import Midi

from google_api.api_calls import create_song_folder, upload_audio_to_drive, share_file_permission

class Command(BaseCommand):
    help = 'Backup midis to google drive'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Midi backup started'))

        for midi in Midi.objects.all():
            if (midi.drive_view_link is None) or (midi.drive_view_link == ""):
                self.stdout.write(self.style.SUCCESS('Backing up {}'.format(midi.__str__())))
                song = midi.song
                part = midi.part
                description = midi.description
                extension = midi.fformat
                file_path = settings.BASE_DIR + midi.media_file.url

                # get of create drive folder
                folder_id = song.drive_folder_id
                if (folder_id is None) or (folder_id == ""):
                    folder_name = "{}-{}".format(song.pk, slugify(song.title))
                    folder_id = create_song_folder(folder_name)
                    song.drive_folder_id = folder_id
                    song.save(update_fields=['drive_folder_id'])

                # build drive metadata
                midi_metadata = {}
                midi_metadata['parents'] = [folder_id]
                midi_metadata['description'] = "{}, {}: {}".format(song.title, part.name, description)
                midi_metadata['viewersCanCopyContent'] = True
                midi_metadata['name'] = file_path.rsplit('/')[-1]

                if extension == "mp3":
                    mimetype = "audio/mpeg"
                else:
                    mimetype = 'audio/mid'

                file_resource = upload_audio_to_drive(midi_metadata, file_path, mimetype)

                midi.drive_view_link = file_resource.get('webViewLink')
                midi.drive_download_link = file_resource.get('webContentLink')
                midi.save(update_fields=['drive_view_link', 'drive_download_link'])
                share_file_permission(file_resource.get('id')) # make shareable
            else:
                self.stdout.write(self.style.NOTICE('{} already backed up. Continue'.format(midi.__str__())))
                continue
        self.stdout.write(self.style.SUCCESS('Midi backup completed successfully'))
