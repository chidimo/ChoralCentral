from django.core.management.base import BaseCommand, CommandError

from song_media.models import Score, Midi

from google_api.api_calls import (
    create_song_folder, upload_pdf_to_drive, upload_audio_to_drive, share_file_permission,
    get_youtube_video_id, get_video_information, get_playlist_id, add_video_to_playlist
)


class Command(BaseCommand):
    help = 'Backup scores and midis to google drive'

    def add_arguments(self, parser):
        parser.add_argument('-quota', type=int)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start resetting api siteusers'))
        if options['quota']:
            quota = options['quota']
        else:
            quota = 10
        siteusers = SiteUser.objects.all()
        for siteuser in siteusers:
            siteuser.quota = quota
            siteuser.used = 0
            siteuser.save(update_fields=['quota', 'used'])
        self.stdout.write(self.style.SUCCESS('Done resetting api siteusers'))

    def form_valid(self, form):
        uploader = self.request.user.siteuser
        song = form.instance.song
        notation = form.instance.notation
        part = form.instance.part
        media_object = form.instance.media_file

        # get of create drive folder
        folder_id = song.drive_folder_id
        if (folder_id is None) or (folder_id == ""):
            folder_name = "{}-{}".format(song.pk, slugify(song.title))
            folder_id = create_song_folder(folder_name)
            song.drive_folder_id = folder_id
            song.save(update_fields=['drive_folder_id'])

        score_metadata = {}
        score_metadata['parents'] = [folder_id]
        score_metadata['name'] = song.title + ".pdf"
        score_metadata['description'] = "{}, {} {}".format(song.title, notation.name, part.name)
        score_metadata['viewersCanCopyContent'] = True

        # create a unique temporary pdf id to avoid race conditions
        pdf_id = str(uuid.uuid4())

        # make a temporary folder in '/media/' folder
        tmp = os.path.join(settings.BASE_DIR, 'media', 'tmp')
        if not os.path.exists(tmp):
            os.mkdir(tmp)
        temp_save_name = 'tmp/' + pdf_id + ".pdf"

        # temporarily write file to disk
        with default_storage.open(temp_save_name, 'wb+') as fh:
            for chunk in media_object.chunks():
                fh.write(chunk)

        temp_pdf_name = str(os.path.join(tmp, pdf_id))
        temp_pdf_path = temp_pdf_name + ".pdf"

        # generate thumbnail
        cmd = "pdftoppm -png -f 1 -singlefile {} {}".format(temp_pdf_path, temp_pdf_name)
        os.system(cmd)

        score = Score.objects.create(
            uploader=uploader, song=song, notation=notation,
            part=part, thumbnail=File(open(temp_pdf_name + ".png", "rb")))

        file_resource = upload_pdf_to_drive(score_metadata, temp_pdf_path)

        # tmp folder is cleaned up once a day by scheduled task.

        score.fsize = file_resource.get('size')
        score.drive_view_link = file_resource.get('webViewLink')
        score.drive_download_link = file_resource.get('webContentLink')
        score.embed_link = file_resource.get('webViewLink').replace('view?usp=drivesdk', 'preview')
        score.save(update_fields=['drive_view_link', 'drive_download_link', 'fsize', 'embed_link'])
        share_file_permission(file_resource.get('id')) # make shareable

        messages.success(self.request, "Score successfully added to {}".format(song.title))
        return redirect(song.get_absolute_url())
