"""views"""

import os
from django.http import FileResponse
from django.conf import settings
from django.views import generic, View
from django.shortcuts import reverse, render
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django_addanother.views import CreatePopupMixin

from .models import VocalPart, ScoreNotation, Score, Midi, VideoLink
from .forms import (
    NewScoreForm, NewMidiForm, NewVideoLinkForm,
    NewVocalPartForm, NewScoreNotationForm
    )

from siteuser.models import SiteUser

class NewVocalPart(LoginRequiredMixin, CreatePopupMixin, generic.CreateView):
    model = VocalPart
    form_class = NewVocalPartForm
    template_name = 'song_media/part_new.html'

class NewScoreNotation(LoginRequiredMixin, CreatePopupMixin, generic.CreateView):
    model = ScoreNotation
    form_class = NewScoreNotationForm
    template_name = 'song_media/notation_new.html'

class NewScore(LoginRequiredMixin, generic.CreateView):
    template_name = 'song_media/score_new.html'
    form_class = NewScoreForm

    def form_valid(self, form):
        form.instance.uploader = SiteUser.objects.get(user=self.request.user)
        self.object = form.save()
        self.object.likes.add(SiteUser.objects.get(user=self.request.user))
        return redirect(self.get_success_url())

    def get_form_kwargs(self):
        """include 'user' and 'pk' in the kwargs to be sent to form"""
        kwargs = super(NewScore, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs.get('pk', None)
        return kwargs

def show_score(self, request, *args, **kwargs):
    doc = get_object_or_404(Score, pk=self.kwargs.get('pk', None))
    doc.downloads += 1
    doc.save()
    fname = doc.media_file.url
    path = os.path.abspath(settings.BASE_DIR + fname)
    response = FileResponse(open(path, 'rb'), content_type="application/pdf")
    response["Content-Disposition"] = "filename={}_{}".format(doc.part, fname)
    return response

class DeleteScore(LoginRequiredMixin, generic.DeleteView):
    model = Score
    template_name = "song_media/score_delete.html"

    def get_success_url(self):
        return reverse("song:detail", kwargs={'pk' : self.kwargs['song_pk'], 'slug' : self.kwargs['slug']})

class NewMidi(LoginRequiredMixin, CreatePopupMixin, generic.CreateView):
    template_name = 'song_media/midi_new.html'
    form_class = NewMidiForm

    def form_valid(self, form):
        form.instance.uploader = SiteUser.objects.get(user=self.request.user)
        self.object = form.save()
        self.object.likes.add(SiteUser.objects.get(user=self.request.user))
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
    response["Content-Disposition"] = "filename={}_{}".format(sound.part, fname)
    return response

class DeleteMidi(LoginRequiredMixin, generic.DeleteView):
    model = Midi
    template_name = "song_media/midi_delete.html"

    def get_success_url(self):
        return reverse("song:detail", kwargs={'pk' : self.kwargs['song_pk'], 'slug' : self.kwargs['slug']})

class NewVideoLink(LoginRequiredMixin, CreatePopupMixin, generic.CreateView):
    model = VideoLink
    template_name = 'song_media/videolink_new.html'
    form_class = NewVideoLinkForm

    def form_valid(self, form):
        form.instance.uploader = SiteUser.objects.get(user=self.request.user)
        return super(NewVideoLink, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(NewVideoLink, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs.get('pk', None)
        return kwargs
