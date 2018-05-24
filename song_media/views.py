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

from google_api.api_calls import get_youtube_video_id, get_video_information, get_playlist_id, add_video_to_playlist

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

class NewScoreNotation(LoginRequiredMixin, SuccessMessageMixin, CreatePopupMixin, generic.CreateView):
    model = ScoreNotation
    form_class = NewScoreNotationForm
    template_name = 'song_media/notation_new.html'
    success_message = "Notation added successfully !"

class NewScore(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'song_media/score_new.html'
    form_class = NewScoreForm

    def form_valid(self, form):
        form.instance.uploader = self.request.user.siteuser
        self.object = form.save()
        song = self.object.song

        relative_media_path = self.object.media_file.url
        full_media_path = settings.BASE_DIR + relative_media_path
        thumbnail_name = full_media_path.replace('.pdf', '')

        # generate thumbnail
        cmd = "pdftoppm -png -f 1 -singlefile {} {}".format(full_media_path, thumbnail_name)
        os.system(cmd)

        thumbnail_file = thumbnail_name + '.png'

        content = File(open(thumbnail_file, "rb"))
        self.object.fsize = os.path.getsize(full_media_path)
        self.object.thumbnail.save(song.title + '.png', content, save=True)
        self.object.save()
        os.remove(thumbnail_file)

        messages.success(self.request, "Score successfully added to {}".format(song.title))
        return redirect(song.get_absolute_url())

    def get_form_kwargs(self):
        """include 'user' and 'pk' in the kwargs to be sent to form"""
        kwargs = super(NewScore, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs.get('pk', None)
        return kwargs

def show_score(request, pk):
    """Display pdf score stored locally by django"""
    score = get_object_or_404(Score, pk=pk)
    score.downloads += 1
    score.save(update_fields=['downloads'])
    path = os.path.abspath(settings.BASE_DIR + score.media_file.url)
    response = FileResponse(open(path, 'rb'), content_type="application/pdf")
    response["Content-Disposition"] = "filename={}.pdf".format(slugify(score.__str__()))
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
        form.instance.uploader = self.request.user.siteuser
        self.object = form.save()
        song = self.object.song
        relative_media_path = self.object.media_file.url
        full_media_path = settings.BASE_DIR + relative_media_path
        self.object.fsize = os.path.getsize(full_media_path)
        extension = os.path.splitext(relative_media_path)[1]

        with open("ext.txt", "w+") as fh:
            fh.write(extension)

        if extension.startswith(".mp3"):
            self.object.fformat = "mp3"
        if extension.startswith(".mid"):
            self.object.fformat = "midi"

        self.object.fsize = os.path.getsize(full_media_path)
        self.object.save(update_fields=['fsize', 'fformat'])

        messages.success(self.request, "Midi successfully added to {}".format(song.title))
        return redirect(song.get_absolute_url())

    def get_form_kwargs(self):
        kwargs = super(NewMidi, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs.get('pk', None)
        return kwargs

def play_mp3(request, pk):
    context = {}
    template = 'song_media/playmp3.html'
    sound = Midi.objects.get(pk=pk)
    sound.downloads += 1
    sound.save(update_fields=['downloads'])
    context['sound'] = sound
    return render(request, template, context)

def download_midi(self, pk):
    sound = get_object_or_404(Midi, pk=pk)
    sound.downloads += 1
    sound.save(update_fields=['downloads'])
    path = os.path.abspath(settings.BASE_DIR + sound.media_file.url)
    response = FileResponse(open(path, 'rb'), content_type="sound/midi")
    file_download_name = "{}.{}".format(slugify(sound.__str__()), sound.fformat)
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

    def get_form_kwargs(self):
        kwargs = super(NewVideoLink, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs.get('pk', None)
        return kwargs

    def form_valid(self, form):
        form.instance.uploader = self.request.user.siteuser
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
