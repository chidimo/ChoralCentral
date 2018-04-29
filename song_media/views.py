"""views"""

import os
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

from django_addanother.views import CreatePopupMixin

from googledrive.api_calls import (upload_score_to_drive, share_file_permission)
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
        form.instance.uploader = SiteUser.objects.get(user=self.request.user)

        # build drive metadata https://developers.google.com/drive/v3/reference/files#resource
        score_metadata = {}
        score_metadata['name'] = form.instance.song.title
        score_metadata['description'] = "{}, {} {}".format(
            form.instance.song.title, form.instance.notation.name, form.instance.part.name)
        score_metadata['parents'] = [CHORAL_SCORE_FOLDER_ID]
        score_metadata['viewersCanCopyContent'] = True

        # change this path to read direct from disk, so as not to save copy in /media/
        self.object = form.save()
        path = os.path.abspath(settings.BASE_DIR + self.object.media_file.url)
        file = upload_score_to_drive(score_metadata, path)

        self.object.drive_view_link = file.get('webViewLink')
        self.object.drive_download_link = file.get('webContentLink')
        self.object.pdf_embed_link = file.get('webViewLink').replace('view?usp=drivesdk', 'preview')
        self.object.save(update_fields=['drive_view_link', 'drive_download_link', 'pdf_embed_link'])
        share_file_permission(file.get('id')) # make shareable

        with open('thumb.txt', 'w+') as fh:
            fh.write("hasThumbnail: ")
            fh.write(str(file.get('hasThumbnail')))
            fh.write("\n\n")
            fh.write("thumbnailLink: ")
            fh.write(str(file.get('thumbnailLink')))
            fh.write("\n\n")
            fh.write("webContentLink: ")
            fh.write(str(file.get('webContentLink')))

        # self.object.thumbnail = File(open(file.get('thumbnailLink'), "rb"))

        self.object.likes.add(SiteUser.objects.get(user=self.request.user))
        messages.success(self.request, "Score successfully added to {}".format(self.object.song.title))
        return redirect(self.get_success_url())

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
        return reverse("song:detail", kwargs={'pk' : self.kwargs['song_pk'], 'slug' : self.kwargs['slug']})

class MidiIndex(LoginRequiredMixin, generic.ListView):
    model = Midi
    context_object_name = 'midis'
    template_name = 'song_media/midi_index.html'

class NewMidi(LoginRequiredMixin, SuccessMessageMixin, CreatePopupMixin, generic.CreateView):
    template_name = 'song_media/midi_new.html'
    form_class = NewMidiForm

    def form_valid(self, form):
        form.instance.uploader = SiteUser.objects.get(user=self.request.user)

        # build drive metadata
        midi_metadata = {}
        midi_metadata['name'] = form.instance.song.title
        midi_metadata['description'] = "{}, {}".format(
            form.instance.song.title, form.instance.part.name)
        midi_metadata['parents'] = [CHORAL_MIDI_FOLDER_ID]

        self.object = form.save()
        path = os.path.abspath(settings.BASE_DIR + self.object.media_file.url)
        file = upload_score_to_drive(midi_metadata, path)
        self.object.drive_view_link = file.get('webViewLink')
        self.object.save(update_fields=['drive_view_link'])
        share_file_permission(file.get('id')) # make shareable

        self.object.likes.add(SiteUser.objects.get(user=self.request.user))
        messages.success(self.request, "Midi successfully added to {}".format(self.object.song.title))
        return redirect(self.get_success_url())

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
        return reverse("song:detail", kwargs={'pk' : self.kwargs['song_pk'], 'slug' : self.kwargs['slug']})

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
