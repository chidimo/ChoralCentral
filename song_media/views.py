"""views"""

import os
from django.http import FileResponse
from django.conf import settings
from django.views import generic, View
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
        score_doc = get_object_or_404(Score, pk=self.kwargs.get('pk', None))
        fname = os.path.basename(score_doc.file.url)
        path = os.path.join(settings.MEDIA_ROOT, 'scores\\' + fname)
        response = FileResponse(open(path, 'rb'), content_type="application/pdf")
        response["Content-Disposition"] = "filename={}_{}".format(score_doc.part, fname)
        return response

class NewMidi(LoginRequiredMixin, CreatePopupMixin, generic.CreateView):
    model = Midi
    template_name = 'song_media/midi_new.html'
    form_class = NewMidiForm

    # def form_valid(self, form): implement likes first
    #     form.instance.uploader = SiteUser.objects.get(user=self.request.user)
    #     self.object = form.save()
    #     self.object.likes.add(SiteUser.objects.get(user=self.request.user))
    #     return redirect(self.get_success_url())

    def form_valid(self, form):
        form.instance.uploader = SiteUser.objects.get(user=self.request.user)
        return super(NewMidi, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(NewMidi, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs.get('pk', None)
        return kwargs

class PlayMidi(View):
    def get(self, request, *args, **kwargs):
        midi = get_object_or_404(Midi, pk=self.kwargs.get('pk', None))
        fname = os.path.basename(midi.file.url)
        path = os.path.join(settings.MEDIA_ROOT, 'midi\\' + fname)
        response = FileResponse(open(path, 'rb'), content_type="audio/midi")
        response["Content-Disposition"] = "filename={}_{}".format(midi.part, fname)
        return response

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
