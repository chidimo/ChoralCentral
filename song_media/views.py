"""views"""

import os
import uuid
from django.http import FileResponse
from django.conf import settings
from django.views import generic
from django.shortcuts import reverse, render
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.defaultfilters import slugify
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django_addanother.views import CreatePopupMixin

from googledrive.api_calls import (
    upload_pdf_to_drive, upload_audio_to_drive, share_file_permission)

from youtube.api_calls import (
    API_ONLY_YOUTUBE, AUTH_YOUTUBE, CHORAL_CENTRAL_CHANNEL_ID,
    get_youtube_video_id, get_video_information,
    get_playlist_id, add_video_to_playlist
)

from siteuser.models import SiteUser

from .models import VocalPart, ScoreNotation, Score, Midi, VideoLink
from .forms import (
    NewScoreForm, NewMidiForm, NewVideoLinkForm,
    NewVocalPartForm, NewScoreNotationForm
    )

CHORAL_SCORE_FOLDER_ID = '138lziNQEspOyyDxObWxtYt8SURDeiVor'
CHORAL_MIDI_FOLDER_ID = '1WYFzgY1Z4l7b39J2pcnq9_m0tY55NBbJ'

class NewVocalPart(LoginRequiredMixin, SuccessMessageMixin, CreatePopupMixin, generic.CreateView):
    model = VocalPart
    form_class = NewVocalPartForm
    template_name = 'song_media/part_new.html'
    success_message = "Vocal part added successfully !"

class ScoreIndex(LoginRequiredMixin, generic.ListView):
    model = Score
    context_object_name = 'scores'
    template_name = 'song_media/score_index.html'

class NewScoreNotation(LoginRequiredMixin, SuccessMessageMixin, CreatePopupMixin, generic.CreateView):
    model = ScoreNotation
    form_class = NewScoreNotationForm
    template_name = 'song_media/notation_new.html'
    success_message = "Notation added successfully !"

class NewScore(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'song_media/score_new.html'
    form_class = NewScoreForm

    def form_valid(self, form):
        uploader = self.request.user.siteuser
        song = form.instance.song
        notation = form.instance.notation
        part = form.instance.part
        media_object = form.instance.media_file

        score_metadata = {}
        score_metadata['name'] = song.title + ".pdf"
        score_metadata['description'] = "{}, {} {}".format(song.title, notation.name, part.name)
        score_metadata['parents'] = [CHORAL_SCORE_FOLDER_ID]
        score_metadata['viewersCanCopyContent'] = True

        # create a unique temporary pdf id to avoid race conditions
        pdf_id = str(uuid.uuid4())

        # make a temporary folder in '/media/' directory
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
        with open("cmd.txt", "w+") as fh:
            fh.write(cmd)
            fh.write("\n\n")
            fh.write(pdf_id)
        os.system(cmd)

        score = Score.objects.create(
            uploader=uploader, song=song, notation=notation,
            part=part, thumbnail=File(open(temp_pdf_name + ".png", "rb")))

        file = upload_pdf_to_drive(score_metadata, temp_pdf_path)

        # tmp folder is cleaned up once a day by scheduled task.

        score.drive_view_link = file.get('webViewLink')
        score.drive_download_link = file.get('webContentLink')
        score.embed_link = file.get('webViewLink').replace('view?usp=drivesdk', 'preview')
        score.save(update_fields=['drive_view_link', 'drive_download_link', 'embed_link'])
        share_file_permission(file.get('id')) # make shareable

        score.likes.add(SiteUser.objects.get(user=self.request.user))
        messages.success(self.request, "Score successfully added to {}".format(song.title))
        return redirect(song.get_absolute_url())

    def get_form_kwargs(self):
        """include 'user' and 'pk' in the kwargs to be sent to form"""
        kwargs = super(NewScore, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs.get('pk', None)
        return kwargs

def show_score(request, pk):
    doc = get_object_or_404(Score, pk=pk)
    doc.downloads += 1
    doc.save()
    path = os.path.abspath(settings.BASE_DIR + doc.media_file.url)
    response = FileResponse(open(path, 'rb'), content_type="application/pdf")
    response["Content-Disposition"] = "filename={}.pdf".format(slugify(doc.__str__()))
    return response

class DeleteScore(LoginRequiredMixin, generic.DeleteView):
    model = Score
    template_name = "song_media/score_delete.html"

    def get_success_url(self):
        score_object = self.get_object()
        song_pk = score_object.song.pk
        song_slug = score_object.song.slug
        return reverse("song:detail", kwargs={'pk' : song_pk, 'slug' : song_slug})

class MidiIndex(LoginRequiredMixin, generic.ListView):
    model = Midi
    context_object_name = 'midis'
    template_name = 'song_media/midi_index.html'

class NewMidi(LoginRequiredMixin, SuccessMessageMixin, CreatePopupMixin, generic.CreateView):
    template_name = 'song_media/midi_new.html'
    form_class = NewMidiForm

    def form_valid(self, form):
        uploader = self.request.user.siteuser
        song = form.instance.song
        description = form.instance.description
        part = form.instance.part
        media_object = form.instance.media_file
        extension = os.path.splitext(media_object.name)[1]

        # build drive metadata
        midi_metadata = {}
        midi_metadata['description'] = "{}, {}: {}".format(
            form.instance.song.title, form.instance.part.name, form.instance.description)
        midi_metadata['parents'] = [CHORAL_MIDI_FOLDER_ID]
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
        file = upload_audio_to_drive(midi_metadata, temp_pdf_path, mimetype)

        midi.fformat = extension
        midi.drive_view_link = file.get('webViewLink')
        midi.drive_download_link = file.get('webContentLink')
        midi.embed_link = file.get('webViewLink').replace('view?usp=drivesdk', 'preview')
        midi.save(update_fields=['drive_view_link', 'drive_download_link', 'fformat', 'embed_link'])
        share_file_permission(file.get('id')) # make shareable

        midi.likes.add(SiteUser.objects.get(user=self.request.user))
        messages.success(self.request, "Midi successfully added to {}".format(song.title))
        return redirect(song.get_absolute_url())

    def get_form_kwargs(self):
        kwargs = super(NewMidi, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs.get('pk', None)
        return kwargs

def play_mp3(request, pk):
    context = {}
    template = 'song_media/play.html'
    sound = get_object_or_404(Midi, pk=pk)

    # check for repeat plays
    sound.downloads += 1
    sound.save()
    context['sound'] = sound
    return render(request, template, context)

def download_midi(self, pk):
    sound = get_object_or_404(Midi, pk=pk)
    sound.downloads += 1
    sound.save()
    fname = sound.media_file.url
    path = os.path.abspath(settings.BASE_DIR + fname)
    response = FileResponse(open(path, 'rb'), content_type="sound/midi")
    file_download_name = slugify("{}_{}".format(sound.part, fname))
    response["Content-Disposition"] = "filename={}".format(file_download_name)
    return response

class DeleteMidi(LoginRequiredMixin, generic.DeleteView):
    model = Midi
    template_name = "song_media/midi_delete.html"

    def get_success_url(self):
        midi_object = self.get_object()
        song_pk = midi_object.song.pk
        song_slug = midi_object.song.slug
        return reverse("song:detail", kwargs={'pk' : song_pk, 'slug' : song_slug})

class NewVideoLink(LoginRequiredMixin, SuccessMessageMixin, CreatePopupMixin, generic.CreateView):
    model = VideoLink
    template_name = 'song_media/videolink_new.html'
    form_class = NewVideoLinkForm
    success_message = "Video link added successfully"

    def form_valid(self, form):
        form.instance.uploader = SiteUser.objects.get(user=self.request.user)
        self.object = form.save()

        song = self.object.song
        playlist_id = song.youtube_playlist_id
        song_title = song.title.strip()
        if (playlist_id is None) or (playlist_id == ''):
            playlist_id = get_playlist_id(AUTH_YOUTUBE, playlist_id, song_title)
            song.youtube_playlist_id = playlist_id
            song.save(update_fields=['youtube_playlist_id'])

        video_id = get_youtube_video_id(self.object.video_link)
        add_video_to_playlist(AUTH_YOUTUBE, video_id, playlist_id)

        video = get_video_information(API_ONLY_YOUTUBE, video_id)
        title = video['items'][0]['snippet']['title']
        youtube_views = video['items'][0]['statistics']['viewCount']
        youtube_likes = video['items'][0]['statistics']['likeCount']

        channel_link = "https://www.youtube.com/watch?list={}&v={}".format(playlist_id, video_id)
        default_thumbnail_url = video['items'][0]['snippet']['thumbnails']['default']['url']

        self.object.channel_link = channel_link
        self.object.title = title
        self.object.youtube_likes = youtube_likes
        self.object.youtube_views = youtube_views
        self.object.thumbnail_url = default_thumbnail_url
        self.object.save()

        return super(NewVideoLink, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(NewVideoLink, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs.get('pk', None)
        return kwargs
