from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.management.base import BaseCommand, CommandError

from song_media.models import Score, Midi

from google_api.api_calls import (
    create_song_folder, upload_pdf_to_drive, upload_audio_to_drive, share_file_permission,
    get_youtube_video_id, get_video_information, get_playlist_id, add_video_to_playlist
)


class Command(BaseCommand):
    help = 'Backup scores and midis to google drive'

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
                self.stdout.write(self.style.SUCCESS('{} already backed up. Continue'.format(score.__str__())))
                continue
        self.stdout.write(self.style.SUCCESS('Score backup completed successfully'))



    def form_valid(self, form):
        uploader = self.request.user.siteuser
        song = form.instance.song
        description = form.instance.description
        part = form.instance.part
        media_object = form.instance.media_file
        extension = os.path.splitext(media_object.name)[1]

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
        midi_metadata['description'] = "{}, {}: {}".format(
            form.instance.song.title, form.instance.part.name, form.instance.description)
        midi_metadata['viewersCanCopyContent'] = True

        tmp = os.path.join(settings.BASE_DIR, 'media', 'tmp')
        if not os.path.exists(tmp):
            os.mkdir(tmp)
        path = 'tmp/' + song.title + extension

        with default_storage.open(path, 'wb+') as destination:
            for chunk in media_object.chunks():
                destination.write(chunk)

        midi = Midi.objects.create(
            uploader=uploader, song=song, part=part, description=description)

        if extension == ".mp3":
            mimetype="audio/mpeg"
            midi_metadata['name'] = song.title + extension
        else:
            midi_metadata['name'] = song.title + extension
            mimetype = 'audio/mid'

        temp_pdf_path = os.path.join(tmp, song.title + extension)
        file_resource = upload_audio_to_drive(midi_metadata, temp_pdf_path, mimetype)

        if extension.startswith(".mp3"):
            midi.fformat = "mp3"
        if extension.startswith(".mid"):
            midi.fformat = "midi"

        midi.fsize = file_resource.get('size')
        midi.drive_view_link = file_resource.get('webViewLink')
        midi.drive_download_link = file_resource.get('webContentLink')
        midi.embed_link = file_resource.get('webViewLink').replace('view?usp=drivesdk', 'preview')
        midi.save(update_fields=['drive_view_link', 'drive_download_link', 'fformat', 'fsize', 'embed_link'])
        share_file_permission(file_resource.get('id')) # make shareable

        messages.success(self.request, "Midi successfully added to {}".format(song.title))
        return redirect(song.get_absolute_url())

