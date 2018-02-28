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

class DisplayScore(View):
    def get(self, request, *args, **kwargs):
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

def play_midi(request, pk):
    context = {}
    template = 'song_media/midi_play.html'
    midi = get_object_or_404(Midi, pk=pk)
    midi.downloads += 1
    midi.save()
    context['midi'] = midi
    return render(request, template, context)

class PlayMidi(View):
    # Later use
    def get(self, request, *args, **kwargs):
        midi = get_object_or_404(Midi, pk=self.kwargs.get('pk', None))
        midi.downloads += 1
        midi.save()
        fname = midi.media_file.url
        path = os.path.abspath(settings.BASE_DIR + fname)
        response = FileResponse(open(path, 'rb'), content_type="audio/midi")
        response["Content-Disposition"] = "filename={}_{}".format(midi.part, fname)
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
