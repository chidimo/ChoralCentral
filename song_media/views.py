"""views"""

import os
import uuid
import json

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

from google_api.api_calls import (
    create_song_folder, upload_pdf_to_drive, upload_audio_to_drive, share_file_permission,
    get_youtube_video_id, get_video_information, get_playlist_id, add_video_to_playlist
)

from siteuser.models import SiteUser

from .models import VocalPart, ScoreNotation, Score, Midi, VideoLink
from .forms import (
    NewScoreForm, NewMidiForm, NewVideoLinkForm,
    NewVocalPartForm, NewScoreNotationForm
    )

class NewVocalPart(LoginRequiredMixin, SuccessMessageMixin, CreatePopupMixin, generic.CreateView):
    model = VocalPart
    form_class = NewVocalPartForm
    template_name = 'song_media/part_new.html'
    success_message = "Vocal part added successfully !"

def admin_media_index(request):
    template = "song_media/admin_media_index.html"
    context = {}
    context['scores'] = Score.objects.all()
    context['midis'] = Midi.objects.all()
    context['siteuser'] = SiteUser.objects.get(user=request.user)
    return render(request, template, context)

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

    def get_form_kwargs(self):
        """include 'user' and 'pk' in the kwargs to be sent to form"""
        kwargs = super(NewScore, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs.get('pk', None)
        return kwargs

# delete later
def preview_score(request, pk):
    score = Score.objects.get(pk=pk)
    score.views += 1
    score.save(update_fields=['views'])
    return redirect(score.embed_link)

def download_score_from_drive(request, pk):
    score = Score.objects.get(pk=pk)
    score.downloads += 1
    score.save(update_fields=['downloads'])
    return redirect(score.drive_download_link)

def show_score(request, pk):
    """Display pdf score stored locally by django"""
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

def download_midi_from_drive(request, pk):
    midi = Midi.objects.get(pk=pk)
    midi.downloads += 1
    midi.save(update_fields=['downloads'])
    return redirect(midi.drive_download_link)

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
        if (playlist_id is None) or (playlist_id == ''):
            playlist_id = get_playlist_id(playlist_id, song.title.strip())
            song.youtube_playlist_id = playlist_id
            song.save(update_fields=['youtube_playlist_id'])

        video_id = get_youtube_video_id(self.object.video_link)
        add_video_to_playlist(video_id, playlist_id)

        video = get_video_information(video_id)
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
